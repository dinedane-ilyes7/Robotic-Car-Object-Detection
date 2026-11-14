"""OpenCV DNN object detection for the 2023–24 ESP32 robotic-car project.

Reconstructed from the report's Python code (pp. 26–27); not a recovered
original. Only renders object bounding boxes/labels. It does NOT drive ESP32.

Requires a compatible externally obtained MobileNet v3 COCO graph,
OpenCV .pbtxt file and corresponding COCO labels text file.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="0", help="Camera index (0) or IP webcam URL")
    parser.add_argument("--weights", type=Path, default=Path("models/frozen_inference_graph.pb"))
    parser.add_argument("--config", type=Path, default=Path("models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"))
    parser.add_argument("--labels", type=Path, default=Path("models/coco.names"))
    parser.add_argument("--confidence", type=float, default=0.45)
    parser.add_argument("--mirror", action="store_true", help="Mirror the video like the report")
    return parser.parse_args()


def read_labels(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Class label file missing: {path}")
    labels = [name.strip() for name in path.read_text(encoding="utf-8").splitlines()]
    labels = [label for label in labels if label]
    if not labels:
        raise ValueError(f"No labels found in {path}")
    return labels


def make_detector(weights: Path, config: Path) -> cv2.dnn_DetectionModel:
    for path in [weights, config]:
        if not path.is_file():
            raise FileNotFoundError(f"Required model file missing: {path}")
    net = cv2.dnn_DetectionModel(str(weights), str(config))
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    return net


def camera_source(source: str) -> int | str:
    return int(source) if source.isdecimal() else source


def main() -> None:
    args = parse_args()
    if not 0.0 < args.confidence <= 1.0:
        raise SystemExit("--confidence must lie between 0 and 1")
    labels = read_labels(args.labels)
    detector = make_detector(args.weights, args.config)
    cap = cv2.VideoCapture(camera_source(args.source))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open webcam stream: {args.source}")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    print("Starting detection. Press Q to exit.")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Frame unavailable; stream disconnected or finished.")
                break
            if args.mirror:
                frame = cv2.flip(frame, 1)
            class_ids, confidences, boxes = detector.detect(
                frame, confThreshold=args.confidence
            )
            if class_ids is None or len(class_ids) == 0:
                class_ids = []
                confidences = []
                boxes = []
            for class_id, confidence, box in zip(
                class_ids.flatten() if len(class_ids) else [],
                confidences.flatten() if len(confidences) else [],
                boxes,
            ):
                idx = int(class_id) - 1
                name = labels[idx] if 0 <= idx < len(labels) else f"class {class_id}"
                x, y, width, height = map(int, box)
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                cv2.putText(
                    frame, f"{name}: {float(confidence):.1%}",
                    (x, max(22, y - 8)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 255, 0), 2,
                )
            cv2.imshow("Robotic Car - Object Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
