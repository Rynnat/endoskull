// Project Bust - K1 MG996R tork + bosluk testi (Uno + Servo.h, PCA gerekmez)
// Baglanti: servo sinyal -> D9, servo + / - -> 5 V 5 A adaptor (Uno'nun 5V'una BAGLAMA), adaptor GND <-> Uno GND ortak.
// Seri monitor 115200, satir sonu "Newline":
//   1500      -> 1500 us'ye git (500..2500)
//   + / -     -> 10 us adim     ++ / --  -> 1 us adim
//   c         -> 1500 us (merkez)   d -> servoyu birak (detach, tork yok)
// Kolu yatay getirmek icin +/- ile kadranda "0"i bul; o degeri forma yaz.
#include <Servo.h>

Servo s;
int us = 1500;

void git(int v) {
  us = constrain(v, 500, 2500);
  if (!s.attached()) s.attach(9, 500, 2500);
  s.writeMicroseconds(us);
  Serial.print(F("servo us = ")); Serial.println(us);
}

void setup() {
  Serial.begin(115200);
  Serial.println(F("K1 tork testi: sayi = us, +/- 10 us, ++/-- 1 us, c = 1500, d = birak"));
  git(1500);
}

void loop() {
  if (!Serial.available()) return;
  String k = Serial.readStringUntil('\n'); k.trim();
  if (k == "+") git(us + 10);
  else if (k == "-") git(us - 10);
  else if (k == "++") git(us + 1);
  else if (k == "--") git(us - 1);
  else if (k == "c") git(1500);
  else if (k == "d") { s.detach(); Serial.println(F("servo birakildi")); }
  else if (k.length() && isDigit(k[0])) git(k.toInt());
}
