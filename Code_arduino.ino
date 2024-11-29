int fsrPin = A0; // FSR connecté à A0
int fsrValue = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  fsrValue = analogRead(fsrPin); // Lecture de la valeur du capteur
  Serial.println(fsrValue);      // Affichage sur le moniteur série
}
