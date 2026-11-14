# Object-detection model files (not included)

The original report references the following files from an **SSD MobileNet v3 Large COCO** model used through OpenCV DNN:

- `frozen_inference_graph.pb` — frozen TensorFlow graph
- `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt` — matching OpenCV graph-text configuration
- `coco.names` — matching, correctly ordered class labels

These model assets were not provided in the report/poster and **cannot be recovered from a screenshot of the Python script**. Obtain a licensed, compatible model/config/label set from their respective publishers or your original backup; place the three files here. Do not mix model configuration files or label orders from different architectures.

The reconstruction intentionally ships no pretrained weights. The code is **not a complete out-of-the-box live detection run** until valid model files are supplied.
