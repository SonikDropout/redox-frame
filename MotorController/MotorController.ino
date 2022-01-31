
const byte pumpInPins[2] = {PD2, PD3};
byte pumpEnPins[1] = {A0};
byte stirrerInPins[2] = {PD4, PD5};
byte stirrerEnPins[1] = {A1};
byte externalControlPin = A2;
bool isSerialInput = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(externalControlPin, INPUT);
  for (int i = 0; i < sizeof(pumpInPins); ++i) {
    pinMode(pumpInPins[i], OUTPUT);
    pinMode(stirrerInPins[i], OUTPUT);
  }
  for (int i = 0; i < sizeof(pumpEnPins); ++i) {
    pinMode(pumpEnPins[i], OUTPUT);
    pinMode(stirrerEnPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String incomingCommand = Serial.readStringUntil('\n');
    int power = incomingCommand.substring(1).toInt();
    char peripheralID = incomingCommand.charAt(0);
    isSerialInput = (bool)power;
    switch (peripheralID) {
      case 'P':
        setPumpPower(power);
        break;
      case 'S':
        setStirrerPower(power);
        break;
      default:
        Serial.write("ERROR!");
        break;
    }
  } else if (!isSerialInput) {
    setPumpPower(map(analogRead(externalControlPin), 0, 1023, 0, 100));
  }
}

void setPumpPower(int power) {
  if (power == 0) {
    disableMotors(pumpInPins);
  }
  else {
    enableMotors(pumpInPins);
    setMotorSpeed(power, pumpEnPins);
  }
}

void setStirrerPower(int power) {
  if (power == 0) {
    disableMotors(stirrerInPins);
  }
  else {
    enableMotors(pumpInPins);
    setMotorSpeed(power, stirrerEnPins);
  }
}

void enableMotors(byte pins[4]) {
  for (int i = 0; i < 4; i += 2) {
    digitalWrite(pins[i], HIGH);
    digitalWrite(pins[i + 1], LOW);
  }
}

void disableMotors(byte pins[4]) {
  for (int i = 0; i < 4; ++i) {
    digitalWrite(pins[i], LOW);
  }
}

void setMotorSpeed(int speed, byte pins[2]) {
  speed = map(speed, 0, 100, 64, 255);
  analogWrite(pins[1], speed);
  analogWrite(pins[0], speed);
}
