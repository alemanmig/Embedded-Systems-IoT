#define RED     6
#define YELLOW  7
#define GREEN   8

void setup() {
  pinMode(RED,OUTPUT);
  pinMode(YELLOW,OUTPUT);
  pinMode(GREEN,OUTPUT);
}

void loop() {
  digitalWrite(RED,digitalRead(RED)^1);
  digitalWrite(YELLOW,digitalRead(YELLOW)^1);
  digitalWrite(GREEN,digitalRead(GREEN)^1);
  delay(50);
}
