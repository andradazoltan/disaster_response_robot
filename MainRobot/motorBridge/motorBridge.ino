#define MRA 3
#define ER A0
#define MLB 9
#define EL A1

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
  digitalWrite(M1, digitalRead(MLB));
  digitalWrite(M2, digitalRead(MRA));
  analogWrite(E1, analogRead(EL));
  analogWrite(E2, analogRead(ER));
}
