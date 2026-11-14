/*
 * Robotic Car (Object Detection) — reconstructed Bluetooth control firmware.
 *
 * SOURCE: 2023–2024 academic group project (maintained by Ilyes Dinedane)
 * RECONSTRUCTED FROM: 2023–2024 project report code listings (pp. 23–26).
 * NOT THE ORIGINAL FILE. NOT YET TESTED ON PHYSICAL HARDWARE.
 *
 * Four direction GPIO values are taken from the original report.
 * The original L298N ENA and ENB pins were NOT documented. Leave their
 * jumpers installed for full-speed testing, or set the GPIO values below
 * after verifying wiring, then remove the corresponding jumpers.
 *
 * Target: original ESP32-WROOM-32 using Bluetooth Classic SPP.
 */

#include <Arduino.h>
#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

// Documented L298N direction pins
constexpr int IN1 = 14;
constexpr int IN2 = 27;
constexpr int IN3 = 26;
constexpr int IN4 = 25;

// Unknown in original report: configure ONLY after wiring verification.
// -1 means driver ENA/ENB jumpers remain fitted (constant-speed mode).
constexpr int ENA_PIN = -1;
constexpr int ENB_PIN = -1;

constexpr unsigned long COMMAND_TIMEOUT_MS = 3000;
unsigned long lastMotionCommandMs = 0;
bool isMoving = false;
int speedDuty = 150;  // 0..255; effective only with ENA/ENB PWM wired

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  isMoving = false;
}

void setMotorDuty(int duty) {
  speedDuty = constrain(duty, 0, 255);
  // analogWrite is available in Arduino-ESP32 core 2.x and 3.x.
  if (ENA_PIN >= 0) analogWrite(ENA_PIN, speedDuty);
  if (ENB_PIN >= 0) analogWrite(ENB_PIN, speedDuty);
}

// Direction mapping follows the original report's forward/backward/turn
// patterns. If motor group polarity differs on your chassis, verify wiring.
void drive(bool in1, bool in2, bool in3, bool in4) {
  digitalWrite(IN1, in1 ? HIGH : LOW);
  digitalWrite(IN2, in2 ? HIGH : LOW);
  digitalWrite(IN3, in3 ? HIGH : LOW);
  digitalWrite(IN4, in4 ? HIGH : LOW);
  isMoving = true;
  lastMotionCommandMs = millis();
}

void processBluetoothCommand(char cmd) {
  switch (cmd) {
    case 'F': case 'f': drive(false, true,  true, false); break;
    case 'B': case 'b': drive(true,  false, false, true);  break;
    case 'L': case 'l': drive(false, true,  false, true);  break;
    case 'R': case 'r': drive(true,  false, true,  false); break;
    case 'S': case 's': stopMotors(); break;
    // Approximate original duty mappings; exact PWM output requires EN pins.
    case '0': setMotorDuty(100); break;
    case '1': setMotorDuty(110); break;
    case '2': setMotorDuty(120); break;
    case '3': setMotorDuty(130); break;
    case '4': setMotorDuty(140); break;
    case '5': setMotorDuty(150); break;
    case '6': setMotorDuty(180); break;
    case '7': setMotorDuty(200); break;
    case '8': setMotorDuty(220); break;
    case '9': setMotorDuty(240); break;
    case 'q': setMotorDuty(255); break;
    default: return;
  }
  Serial.print("Bluetooth command: ");
  Serial.println(cmd);
}

void setup() {
  Serial.begin(115200);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  if (ENA_PIN >= 0) pinMode(ENA_PIN, OUTPUT);
  if (ENB_PIN >= 0) pinMode(ENB_PIN, OUTPUT);
  stopMotors();
  setMotorDuty(speedDuty);
  SerialBT.begin("RoboticCarESP32");
  Serial.println("RoboticCarESP32 ready. Commands: F B L R S 0..9 q");
  if (ENA_PIN < 0 || ENB_PIN < 0) {
    Serial.println("Warning: ENA/ENB GPIO not configured; speed commands may have no effect.");
  }
}

void loop() {
  while (SerialBT.available() > 0) {
    const char cmd = static_cast<char>(SerialBT.read());
    processBluetoothCommand(cmd);
  }
  // Added during reconstruction: fail-safe for lost/one-shot BT messages.
  if (isMoving && (millis() - lastMotionCommandMs >= COMMAND_TIMEOUT_MS)) {
    stopMotors();
    Serial.println("Motion timeout -> stopped");
  }
  delay(5);
}
