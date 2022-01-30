
const byte pumpInPins[2] = {2, 4};
byte pumpEnPins[1] = {3};
byte stirrerInPins[2] = {5, 7};
byte stirrerEnPins[1] = {6};
byte externalControlPin = 5;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(externalControlPin, INPUT);
  for (int i = 0; i < 4; ++i) {
    pinMode(pumpInPins[i], OUTPUT);
    pinMode(stirrerInPins[i], OUTPUT);
  }
  for (int i = 0; i < 2; ++i) {
    pinMode(pumpEnPins[i], OUTPUT);
    pinMode(stirrerEnPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String incomingCommand = Serial.readStringUntil('\n');
    int power = incomingCommand.substring(1).toInt();
    char peripheralID = incomingCommand.charAt(0);
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
  }
  setPumpPower(analogRead(externalControlPin));
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
