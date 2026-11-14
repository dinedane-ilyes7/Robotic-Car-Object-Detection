# Source reconstruction notes and credit

This project was reconstructed from two user-supplied sources:

1. *Robotic Car (Object Detection)*, 2023–2024 Bachelor's project report (32 printed pages). The Bluetooth sketch appears across printed pages **23–26** and Python object-detection code on printed pages **26–27**. The hardware photograph appears on printed page **20**.
2. *Object Detection Robotic Car*, original academic poster, supervised by Mrs. Mouhouche.

## What was available

- ESP32 GPIO directions: `IN1=14`, `IN2=27`, `IN3=26`, `IN4=25`.
- Bluetooth commands: `F`, `B`, `L`, `R`, `S`, and speed selector `0`–`9` or `q`.
- Hardware concept: ESP32, L298N, 4 DC motors, battery, phone webcam.
- Python OpenCV DNN with confidence `0.45`, an SSD MobileNet v3 graph, `coco.names`, and camera frames at `1280×720`.
- A photo of the physically assembled prototype.

## Reconstruction and modifications

- **Original Arduino/Python files were not supplied.** This repository contains **newly reconstructed files** based on the code listings, not byte-identical recoveries.
- The ESP32 source from the report appeared incomplete regarding PWM channel and enable-pin setup. The reconstructed sketch therefore defaults to full-speed direction control with ENA/ENB jumpers and makes PWM enable pins explicitly configurable.
- We renamed the Bluetooth device from a tutorial-like name in the printed code to `RoboticCarESP32`.
- We added a stop-on-timeout safety mechanism, explanatory warnings, and a serial log.
- The Python file replaces the example phone IP address with command-line configuration, adds missing-file checks, and safely handles missing stream frames.
- We **did not** include actual pretrained model binaries, the original computer environment, hardware test recordings, code for Bluetooth object-coordinate transmission, or autonomous navigation code, because the supplied documents do not contain verifiable complete originals for them.
- **No academic report or poster PDF has been copied into this repository.** The cropped hardware photo is extracted from the original project report and credited to the team.

## Validation status

The rebuilt Python files were syntax-checked and repository references inspected, but the motor code and vision model were **not executed on physical hardware**. Do not treat code reconstruction as proof of identical original behavior.

## Project contributors

This was a **student group project** at IGEE / University of Boumerdes, Algeria, supervised by **Mrs. Mouhouche Faiza**. The GitHub repository is maintained by **Ilyes Dinedane** and does not imply sole authorship of the original work.
