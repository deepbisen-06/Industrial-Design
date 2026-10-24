% ThingSpeak MATLAB Analysis: run via TimeControl once per minute.
% Replace placeholders in your PRIVATE cloud script, never in a shared submission.
weatherChannelID = 0; weatherReadKey = 'YOUR_WEATHER_READ_KEY';
stateChannelID = 0; stateReadKey = 'YOUR_STATE_READ_KEY';
stateWriteKey = 'YOUR_STATE_WRITE_KEY';
alertKey = 'YOUR_THINGSPEAK_ALERTS_API_KEY';
TEMP_HIGH = 35; RH_HIGH = 80;
TEMP_RESET = 34; RH_RESET = 78; % Hysteresis prevents threshold chatter.
COOLDOWN_SECONDS = 1800;

[data, stamps] = thingSpeakRead(weatherChannelID,'Fields',[1 2], ...
    'NumPoints',1,'ReadKey',weatherReadKey);
if isempty(data) || any(~isfinite(data(1,:)))
    disp('No valid sample; no alert decision.'); return;
end
nowUTC = datetime('now','TimeZone','UTC');
stamps.TimeZone = 'UTC';
if seconds(nowUTC-stamps(end)) > 120
    disp('Stale data; no alert decision.'); return;
end
t = data(end,1); h = data(end,2);
if t < -40 || t > 80 || h < 0 || h > 100
    disp('Outside DHT22 range.'); return;
end
% Dedicated state channel avoids collisions with ESP32 weather updates.
% Initialize its first entry: Field1=0, Field2=0 before enabling TimeControl.
state = thingSpeakRead(stateChannelID,'Fields',[1 2], ...
    'NumPoints',1,'ReadKey',stateReadKey);
if isempty(state) || any(~isfinite(state(end,:)))
    error('Initialize the state channel with Field1=0 and Field2=0.');
end
latched = state(end,1) > 0; lastSent = state(end,2);
nowSeconds = posixtime(nowUTC);
high = t > TEMP_HIGH || h > RH_HIGH;
recovered = t <= TEMP_RESET && h <= RH_RESET;
if latched && recovered
    thingSpeakWrite(stateChannelID,[0 lastSent],'Fields',[1 2], ...
        'WriteKey',stateWriteKey);
    disp('Alert rearmed after recovery.');
elseif ~latched && high && nowSeconds-lastSent >= COOLDOWN_SECONDS
    subject = 'ESP32 weather station: threshold exceeded';
    body = sprintf('Temperature %.2f C; humidity %.2f %% RH. Limits: %.1f C / %.1f %% RH. UTC: %s', ...
        t,h,TEMP_HIGH,RH_HIGH,char(nowUTC));
    opts = weboptions('HeaderFields', ...
        {'ThingSpeak-Alerts-API-Key',alertKey},'Timeout',20);
    % If webwrite fails it throws, and no state update occurs.
    webwrite('https://api.thingspeak.com/alerts/send', ...
        'subject',subject,'body',body,opts);
    thingSpeakWrite(stateChannelID,[1 nowSeconds],'Fields',[1 2], ...
        'WriteKey',stateWriteKey);
    disp('Alert request accepted; verify email delivery in the inbox.');
else
    disp('No new alert required.');
end
% Limit: email API + state write are not transactional. A state-write failure
% after an accepted email could cause a duplicate on a later execution.
