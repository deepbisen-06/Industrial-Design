#pragma once
// Copy to config.h and enter LOCAL values. Never commit config.h.
constexpr char WIFI_SSID[] = "YOUR_WIFI_NAME";
constexpr char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";
constexpr char TS_WRITE_KEY[] = "YOUR_CHANNEL_WRITE_API_KEY";
// Paste the current trusted root CA for api.thingspeak.com as a PEM certificate.
// Obtain from the issuing CA's official HTTPS site and verify the certificate chain.
// Empty by default: firmware refuses uploads until TLS trust is configured.
constexpr char TS_ROOT_CA_PEM[] = R"PEM()PEM";
