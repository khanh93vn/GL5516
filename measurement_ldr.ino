#define DEBUG 0
#define DEBUGDELAY 1000 // time of delay each loop

#define VOUTPIN A0 // read Vout
#define LEDPIN 6 // led PWM pin
#define BAUDRATE 115200 // serial communication baudrate

#define RREF 10000.0 // to measure resistance

#define SERIALBUFFERSIZE 4 // size of buffer for serial communication
#define SERIALDELAY 10 // time for signal to be received.
#define VOUTBUFFERSIZE 100 // number of measurements each time

char serialBuffer[SERIALBUFFERSIZE]; // buffer for serial communication
uint16_t voutBuffer[VOUTBUFFERSIZE]; // buffer for measured Vout

void adjustLed();
void readVout();
void sendVout();

void setup() {
  Serial.begin(BAUDRATE);
  pinMode(LEDPIN, OUTPUT);
  pinMode(VOUTPIN, INPUT);
  Serial.println("Arduino is ready!");
}

void loop() {
  #if DEBUG
  // DEBUG MODE
  // display measured value each loop.
  int vo = analogRead(VOUTPIN);
  Serial.print(RREF * (1023.0 - vo) / vo);
  Serial.println(" Ohm");
  adjustLed();
  delay(DEBUGDELAY);

  #else
  // NORMAL OPERATION
  // automatically send measured values in batch
  // each time a serial message is received.
  if(Serial.available()) {
    adjustLed();
    delay(SERIALDELAY);
    readVout();
    sendVout();
  }
  #endif
}

void adjustLed() {
  if(Serial.available()) {
    delay(SERIALDELAY); 
    int i = 0;
    while(Serial.available()) {
      serialBuffer[i++] = Serial.read();
    }

    analogWrite(LEDPIN, atoi(serialBuffer));
  }
}

void readVout() {
  for(int i = 0; i < VOUTBUFFERSIZE; i++) {
    voutBuffer[i] = analogRead(VOUTPIN);
  }
}

void sendVout() {
  Serial.write((uint8_t *) voutBuffer, VOUTBUFFERSIZE*sizeof(uint16_t));
}
