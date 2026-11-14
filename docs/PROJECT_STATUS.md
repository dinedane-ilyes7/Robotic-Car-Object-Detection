# Project status

## Established by the original report/poster

- Four-wheel ESP32/L298N prototype assembled.
- Bluetooth commands used for car movement.
- Smartphone video feed used for detection of objects through OpenCV.
- Arduino IDE and Python used during implementation.

## Included in the reconstructed code package

- Reconstructed, reviewed motor-control sketch using the report's direction GPIOs and command mapping.
- Reconstructed Python object detection viewer with external model and camera settings.
- Wiring guide, project credits, source limitations, extracted robot photo.

## Unavailable / not demonstrated by sources

- Original ESP32 `.ino` or equivalent source file.
- Original Python `.py` file and versioned environment.
- L298N ENA/ENB wiring and actual PWM setup.
- Exact pretrained SSD MobileNet graph, matching `.pbtxt`, and class label file.
- Python-to-ESP32 communications linking detected objects to motor steering.
- Verified fully autonomous obstacle avoidance, path planning, robot learning, or model-training scripts.
- Reproduced latency, detection accuracy, or measured test metrics.

## Potential future additions

The user's later robotic-car work mentioned Wi-Fi/UDP motor control and 3-D visualization, but complete verified original code was not included in the supplied 2023–2024 report. These can be added **as later revisions**, separately attributed and marked with their implementation dates when recovered or recreated.
