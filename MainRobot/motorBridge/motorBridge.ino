#define MRA 2
#define ER 3
#define MLB 8
#define EL 9

#define E1 5           //Left wheel
#define M1 4           //Left wheel
#define E2 6           //Right wheel           
#define M2 7           //Right wheel

void setup() {
  pinMode(M1, OUTPUT);  
  pinMode(M2, OUTPUT);
  pinMode(E1, OUTPUT);  
  pinMode(E2, OUTPUT);

  pinMode(MRA, INPUT);  
  pinMode(MLB, INPUT);
  pinMode(ER, INPUT);  
  pinMode(EL, INPUT);

}

void loop() {
  byte pwm_left = pulseIn(EL, HIGH);
  byte pwm_right = pulseIn(ER, HIGH);

  digitalWrite(M1, digitalRead(MLB));
  digitalWrite(M2, digitalRead(MRA));
  analogWrite(E1, pwm_left);
  analogWrite(E2, pwm_right);
}
