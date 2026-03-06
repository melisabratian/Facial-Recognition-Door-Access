#include <Servo.h>

#define GREEN_LED 13        // LED verde pe pinul 13
#define RED_LED 12          // LED roșu pe pinul 12
#define BUTTON_PIN 3        // Buton conectat la D7
#define SWITCH_PIN_1 2      // Pinul 2 pentru switch (prima poziție)
#define SWITCH_PIN_2 4      // Pinul 4 pentru switch (a doua poziție)

Servo lockServo;            // Obiect Servo pentru motorul servo
int lockOpenPosition = 90;  // Poziția deschisă a servo (90 de grade)
int lockClosePosition = 0;  // Poziția închisă a servo (0 grade)

char litera_p;              // Variabilă pentru a citi caracterele de la calculator

// Variabile pentru a păstra starea anterioară a switch-ului
bool prevSwitchOnPin1 = false;
bool prevSwitchOnPin2 = false;

void setup() {
  // Configurare pini LED-uri
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);

  // Configurare buton
  pinMode(BUTTON_PIN, INPUT);

  // Configurare toggle switch
  pinMode(SWITCH_PIN_1, INPUT_PULLUP);
  pinMode(SWITCH_PIN_2, INPUT_PULLUP);

  // Configurare servo motor
  lockServo.attach(10); // Conectăm servo motorul la pinul digital D10
  lockServo.write(lockClosePosition); // Închidem servo-ul la început

  // Pornire comunicație serială
  Serial.begin(9600);
}

void loop() {
  // Verifică poziția switch-ului
  bool switchOnPin1 = !digitalRead(SWITCH_PIN_1); // LOW înseamnă activ pe pinul 2
  bool switchOnPin2 = !digitalRead(SWITCH_PIN_2); // LOW înseamnă activ pe pinul 4

  // Detectare schimbare poziție pentru pinul 1
  if (switchOnPin1 && !prevSwitchOnPin1) {
    Serial.println('c'); // Trimite doar o dată 'c'
    Serial.flush();      // Golește bufferul serial
  }
  prevSwitchOnPin1 = switchOnPin1; // Actualizare stare anterioară pentru pinul 1

  // Detectare schimbare poziție pentru pinul 2
  if (switchOnPin2 && !prevSwitchOnPin2) {
    Serial.println('q'); // Trimite doar o dată 'q'
    Serial.flush();      // Golește bufferul serial
  }
  prevSwitchOnPin2 = switchOnPin2; // Actualizare stare anterioară pentru pinul 2

  // Verifică butonul și trimite 'd' de fiecare dată când este apăsat
  if (switchOnPin1 && digitalRead(BUTTON_PIN) == LOW) {
    Serial.println('d'); // Trimite 'd' dacă butonul este apăsat
    Serial.flush();      // Golește bufferul serial
    delay(200);          // Mică întârziere pentru stabilitate
  }

  // Așteptăm răspunsul calculatorului
  if (Serial.available() >= 1) {
    litera_p = Serial.read();

    if (litera_p == 'a') {
      // Aprinde LED-ul verde
      digitalWrite(GREEN_LED, HIGH);

      // Activează servo-ul pentru a deschide "ușa"
      lockServo.write(lockOpenPosition);
      delay(3000); // Așteaptă 3 secunde

      // Închide "ușa"
      lockServo.write(lockClosePosition);

      // Stinge LED-ul verde
      digitalWrite(GREEN_LED, LOW);
    } else if (litera_p == 'b') {
      // Aprinde LED-ul roșu
      digitalWrite(RED_LED, HIGH);

      // Așteaptă 2 secunde
      delay(2000);

      // Stinge LED-ul roșu
      digitalWrite(RED_LED, LOW);
    }
    Serial.flush(); // Golește bufferul serial după procesarea caracterului
  }

  delay(100); // Mică întârziere pentru stabilitate
}
