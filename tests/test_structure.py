"""Small offline checks for the reconstructed source archive."""
from pathlib import Path
import ast
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReconstructedProjectTests(unittest.TestCase):
    def test_python_syntax(self):
        source = (ROOT / 'vision/object_detection.py').read_text(encoding='utf-8')
        ast.parse(source)

    def test_hardware_pin_assignments(self):
        source = (ROOT / 'firmware/esp32_bluetooth_car/esp32_bluetooth_car.ino').read_text(encoding='utf-8')
        for pin, name in [(14,'IN1'),(27,'IN2'),(26,'IN3'),(25,'IN4')]:
            self.assertIn(f'constexpr int {name} = {pin};',source)

    def test_camera_parameters(self):
        source = (ROOT / 'vision/object_detection.py').read_text(encoding='utf-8')
        self.assertIn('default=0.45',source)
        self.assertIn('setInputSize(320, 320)',source)

    def test_no_unavailable_model_claim(self):
        self.assertFalse((ROOT / 'models/frozen_inference_graph.pb').exists())
        self.assertTrue((ROOT / 'models/README.md').exists())

if __name__ == '__main__':
    unittest.main()
