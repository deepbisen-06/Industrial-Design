# IoT Weather Station — Deep Bisen

Read report.pdf, then cloud/SETUP.md. Firmware is in firmware/WeatherStation/WeatherStation.ino. A PlatformIO configuration is supplied. Never share the populated config.h or cloud API keys.

This is a prepared implementation and report, NOT a claim of completed hardware/cloud validation. Required real dashboard and email screenshots must be added before final submission; see evidence/README.md. Firmware target compilation, flashing and cloud execution have not been performed. Software-only helper and policy tests passed; their exact scope is in verification/test_results.txt.

To run existing software-only checks:
  g++ -std=c++11 -Wall -Wextra -pedantic verification/test_logic.cpp -o /tmp/iot_logic_test
  /tmp/iot_logic_test
  python verification/test_alert_logic.py

To build on a machine with PlatformIO and network access:
  copy firmware/WeatherStation/config.example.h to firmware/WeatherStation/config.h
  fill local configuration, including trusted CA
  cd firmware
  pio run
  pio run --target upload
  pio device monitor

Alternatively open WeatherStation.ino in Arduino IDE and install the documented libraries.
Report regeneration requires Python, matplotlib, numpy, reportlab, and python-docx:
  python build_report.py

The submission folder follows the assignment name IoT_Weather_Station_Deep_Bisen.
Attach real evidence, update report with actual outcomes,
then ZIP this folder and upload it to Google Drive with the access your instructor requires.
