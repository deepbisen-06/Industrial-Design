# ThingSpeak and ESP32 setup

1. Create a private ThingSpeak weather channel. Name Field 1 `Temperature (C)` and Field 2 `Relative Humidity (%)`. Record the channel ID, Read API key and Write API key privately.
2. Connect a bare DHT22 facing its grille: pin 1 VCC to ESP32 3V3; pin 2 DATA to GPIO4; pin 3 NC; pin 4 GND to GND. Fit a 4.7-10 kOhm pull-up from DATA to 3V3 and a 100 nF decoupling capacitor between VCC/GND. A module's pin order may differ: follow its labels; it may include the pull-up. Never pull GPIO4 to 5 V. Unplug power before wiring.
3. Install Arduino IDE's Espressif ESP32 board package and Adafruit DHT sensor library plus Adafruit Unified Sensor dependency, or use the supplied PlatformIO configuration.
4. Copy `firmware/WeatherStation/config.example.h` to `config.h` in the same folder. Set Wi-Fi SSID/password and weather-channel Write API key. Use 2.4 GHz Wi-Fi supported by the ESP32.
5. Configure the current trusted root CA for `api.thingspeak.com` in TS_ROOT_CA_PEM. Obtain the root from the issuing CA's official HTTPS site and check the server chain using your browser certificate viewer. Include multiple trusted root PEMs if needed for an announced rotation. Do not paste the expiring leaf as a permanent trust root or disable certificate validation. NTP access to pool.ntp.org / time.nist.gov is needed to establish correct clock time before TLS.
6. Select ESP32 Dev Module / the matching board and serial port, compile and upload WeatherStation.ino. Serial Monitor baud is 115200. Wait at least 20 seconds for the first upload. `Upload accepted: entry N` with N>0 confirms an accepted API write; HTTP 200 with body 0 is a rejected write. Check the same entry on the cloud channel. Firmware samples every 2.5 seconds and attempts upload every 20 seconds (conservative relative to the usual 15-second free-channel interval; confirm your account's current limits).
7. In the channel's Private View, add charts for Field 1 and Field 2, label their axes with C and % RH, choose a useful time range, and enable available automatic refresh. An updating chart is near-real-time, not continuous streaming.
8. For email state persistence, create a SECOND private channel with Field 1 `Alert latch` and Field 2 `Last alert Unix seconds`. Initialize it manually with one valid entry, Field1=0 and Field2=0, using its Write API key. Do not use the weather channel for this state.
9. Under ThingSpeak Apps > MATLAB Analysis create a script using cloud/threshold_email.m. Supply weather/state channel IDs and their private keys. Obtain your account's ThingSpeak Alerts API key in the appropriate account/API-key settings and use it only in the private script. Verify the account email and availability/limits of the Alerts API for your account.
10. Execute the analysis once manually, inspect output, and then use Apps > TimeControl to run that analysis every minute if supported by your account. Use the shortest available interval otherwise and document the resulting delay. Default high thresholds are temperature >35 C OR RH >80%. Rearm requires temperature <=34 C AND RH <=78%, plus a 30-minute interval between successful sends. Equality at the high limit does not trigger.
11. Test with genuine readings if possible. Alternatively use a separate test channel with explicitly labelled synthetic values, or temporarily lower the threshold below the current measured value. Restore production limits after testing. Do not call synthetic readings measured data.
12. Capture your actual dashboard, accepted serial upload, MATLAB result, and received email. Redact all API keys and private email addresses before sharing. Follow evidence/README.md. Account permissions, email delivery, cloud execution, and hardware behavior must be verified locally.

Useful official references (consult for current UI, quotas and TLS chain):
- https://www.mathworks.com/help/thingspeak/
- https://www.mathworks.com/help/thingspeak/alerts-api.html
- https://docs.espressif.com/projects/arduino-esp32/en/latest/
- https://github.com/adafruit/DHT-sensor-library

Network destinations: api.thingspeak.com over HTTPS; NTP servers over UDP/123; board/library registries during tool installation. Email is sent by the cloud; no SMTP password is needed on the ESP32. Keys/passwords are intentionally absent from this submission.
