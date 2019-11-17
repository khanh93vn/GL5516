/**
 * Code do do lap quang tro
 * 
 * Board Arduino chi do va gui gia tri Vout khi nhan duoc tin hieu tu
 * may tinh.
 */

// ---------------------------------------------------------------------------
// Khai bao hang so

#define DEBUG 0

// 2 chan do dien tro:
#define VOUTPIN1 A0
#define VOUTPIN2 A1

// Baudrate:
#define BAUDRATE 115200

// So milli giay delay moi vong lap:
#define LOOPDELAY 100

// Thoi gian chop LED canh bao loi:
#define BLINKDELAY 400

// So lan chop LED canh bao loi:
#define BLINKTIMES 10

// Cac hang so khac:
#define VOUTBUFFERSIZE 100 // number of measurements each time

// ---------------------------------------------------------------------------
// Khai bao bien global

uint16_t voutBuffer1[VOUTBUFFERSIZE]; // buffer for measured Vout1
uint16_t voutBuffer2[VOUTBUFFERSIZE]; // buffer for measured Vout2

// ---------------------------------------------------------------------------
// Function prototypes

void blink_led(); // nhap nhay LED canh bao khi xay ra loi
void readVouts(); // do cac gia tri Vout
void sendVouts(); // gui cac gia tri Vout ve may tinh

// ---------------------------------------------------------------------------
// Main

void setup() {
  // Khoi tao:
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(VOUTPIN1, INPUT);
  pinMode(VOUTPIN2, INPUT);

  // Bat dau ket noi:
  Serial.begin(BAUDRATE);

  // Quan trong: may tinh chi bat dau cong viec sau khi nhan duoc dong nay:
  Serial.println("Arduino is ready!");
}

void loop() {
  if(Serial.available()) {
    char c = Serial.read();
    if(c != 'm') { // chi do khi nhan duoc tin hieu la ky tu 'm'
      blink_led(); // nhap nhay LED de bao loi
      return; // skip vong lap
    }
    
    readVouts(); // do Vout
    sendVouts(); // gui ve may tinh
  }

  delay(LOOPDELAY);
}

// ---------------------------------------------------------------------------
// Functions

void blink_led() {
  for(int i = 0; i < BLINKTIMES; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(BLINKDELAY);
    digitalWrite(LED_BUILTIN, LOW);
    delay(BLINKDELAY);
  }
}

void readVouts() {
  for(int i = 0; i < VOUTBUFFERSIZE; i++) {
    voutBuffer1[i] = analogRead(VOUTPIN1);
    voutBuffer2[i] = analogRead(VOUTPIN2);
  }
}

void sendVouts() { // Gui Vout duoi dang chuoi
  Serial.write((uint8_t *) voutBuffer1, VOUTBUFFERSIZE*sizeof(uint16_t));
  Serial.write((uint8_t *) voutBuffer2, VOUTBUFFERSIZE*sizeof(uint16_t));
}
