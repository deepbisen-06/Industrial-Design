#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <time.h>
#include "config.h"
#include "logic.h"

constexpr uint8_t DHT_PIN=4;
constexpr uint32_t SAMPLE_MS=2500, UPLOAD_MS=20000, WIFI_RETRY_MS=15000;
DHT dht(DHT_PIN,DHT22);
uint32_t sampleAt=0, uploadAt=0, wifiAt=0;
float temperature=NAN, humidity=NAN;
bool sampleReady=false;

void setup() {
 Serial.begin(115200); dht.begin();
 WiFi.mode(WIFI_STA); WiFi.setAutoReconnect(true);
 WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
 configTime(0,0,"pool.ntp.org","time.nist.gov");
 Serial.println("Weather station started. Waiting for Wi-Fi/time and sensor warm-up.");
}
void loop() {
 uint32_t now=millis();
 if(WiFi.status()!=WL_CONNECTED && due(now,wifiAt,WIFI_RETRY_MS)) {
  wifiAt=now; WiFi.reconnect(); Serial.println("Wi-Fi reconnect requested");
 }
 if(due(now,sampleAt,SAMPLE_MS)) {
  sampleAt=now; float h=dht.readHumidity(),t=dht.readTemperature();
  sampleReady=validReading(t,h);
  if(sampleReady) {temperature=t;humidity=h;Serial.printf("T=%.2f C RH=%.2f %%\n",t,h);}
  else Serial.println("Sensor invalid; this sample will not be uploaded");
 }
 if(!due(now,uploadAt,UPLOAD_MS)) {delay(10);return;}
 uploadAt=now; // Also rate-limit failed attempts.
 if(WiFi.status()!=WL_CONNECTED||!sampleReady) return;
 if(time(nullptr)<1700000000) {Serial.println("Waiting for NTP time before TLS");return;}
 if(TS_ROOT_CA_PEM[0]=='\0') {Serial.println("Configure trusted root CA; upload blocked");return;}
 WiFiClientSecure tls; tls.setCACert(TS_ROOT_CA_PEM); tls.setHandshakeTimeout(10);
 HTTPClient http; http.setConnectTimeout(10000); http.setTimeout(10000);
 if(!http.begin(tls,"https://api.thingspeak.com/update")) {
  Serial.println("HTTPS initialization failed");return;
 }
 http.addHeader("Content-Type","application/x-www-form-urlencoded");
 String body="api_key="+String(TS_WRITE_KEY)+"&field1="+String(temperature,2)+"&field2="+String(humidity,2);
 int status=http.POST(body); String reply=status>0?http.getString():"";
 // ThingSpeak returns a positive entry ID on success; HTTP 200 with 0 is failure.
 long entry=reply.toInt();
 if(status==200&&entry>0) Serial.printf("Upload accepted: entry %ld\n",entry);
 else Serial.printf("Upload failed: HTTP %d; entry %ld\n",status,entry);
 http.end();
}
