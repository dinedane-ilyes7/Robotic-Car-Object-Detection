# Original hardware and wiring notes

Information below is transcribed from the team's academic project report (hardware chapter, wiring image, and embedded motor-control listing).

| Item | Project description |
|---|---|
| Controller | ESP32-WROOM-32 |
| Motor driver | L298N dual H-bridge |
| Motors | Four geared DC drive motors, connected as left/right groups |
| Camera | Phone running an IP Webcam video-stream application |
| Battery | Battery-holder arrangement described around nominal 7.4 V (two lithium-ion cells in series) |
| Software | Arduino IDE for ESP32 firmware; Python + OpenCV on computer for vision |

## Documented ESP32-to-driver direction pins

| ESP32 GPIO | L298N input |
|---|---|
| GPIO 14 | IN1 |
| GPIO 27 | IN2 |
| GPIO 26 | IN3 |
| GPIO 25 | IN4 |

**ENA and ENB pin mapping is NOT identified in the report.** The code listing mentions PWM channels but does not show complete `ledcSetup`/`ledcAttachPin` initialization. Consequently it is not possible to reconstruct authentic motor-speed PWM wiring from the report alone.

The sketch defaults ENA/ENB to `-1`, allowing constant-speed testing with the motor-driver enable jumpers fitted. To implement variable speed, verify physical hardware wiring, remove EN jumpers, assign two available PWM-capable GPIOs in the firmware, and test each side on a lifted chassis at low duty cycle.

## Safety for bench tests

- Disconnect motors or raise the wheels before trying direction commands.
- Use a suitable motor power supply matching the driver/motors and a common ground between ESP32 and driver.
- Do **not** feed motor voltage directly into ESP32 GPIO or 3.3 V logic pins.
- Never connect rechargeable lithium cells to an improper charging source. Use appropriate protection and charger.
- Observe the new firmware's 3-second stop-on-command-timeout behavior; the initial project code did not show this additional failsafe.
- Do not claim obstacle avoidance: camera detections and Bluetooth motor controls are separate systems in the recovered source.
