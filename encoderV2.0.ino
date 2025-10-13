// Includes
#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>

// Defines
#define pinoCLK      6
#define pinoDT       7
#define botaoSetup   8
#define frequencia   60 // Frequência do servo
#define SERVOMIN     150 // Valor mínimo do servo
#define SERVOMAX     450 // Valor máximo do servo


// Variáveis globais
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
void beginServos();
int atualCLK; // CLK ---> Pino 5 do encoder
int anteriorCLK;
int DT;       // DT  ---> Pino 4 do encoder(verificação de posição)
int anterioresCLK[5] = {0, 0, 0, 0, 0};
float posDedo[5] = {0, 0, 0, 0, 0};
float posDedoMax[5] = {0, 0, 0, 0, 0};



void setup() {

  Adafruit_PWMServoDriver();
  beginServos();
  delay(100);
  Serial.begin(9600);
  pinMode(pinoCLK, INPUT);
  pinMode(pinoDT, INPUT);
  pinMode(botaoSetup, INPUT);
  anteriorCLK = digitalRead(pinoDT);

}



void loop() {
  
    while(digitalRead(botaoSetup) == 0){} // Espera com que o usuário aperte o botão (Mão fechada)
    delay(1000);
    
    while(digitalRead(botaoSetup) == 0){  // Espera com que o usuário aperte o botão (Mão aberta)
      encoderUpdate(pinoCLK, pinoDT, 0, 1);
    }

    posDedoMax[0] = posDedo[0];           // Define os valores máximos 

    while(1){

      if(posDedo[0] > 500){               // Restaura o valor caso passe do máximo
        posDedo[0] = 500;
      }
      if(posDedo[0] < 0){                 // Restaura o valor caso passe do mínimo
        posDedo[0] = 0;
      }
      encoderUpdate(pinoCLK, pinoDT, 0, (500/posDedoMax[0]));
      Serial.println(posDedo[0]);
      writeServos(0, (int)(posdedo[0] * 0,6 + 150) ) // Transmite o valor convertido ao servo

  
    
    
  }


void writeServos(int nServo, int posicao) {

  int pos = map ( posicao , 0 , 180 , SERVOMIN, SERVOMAX);
  pwm.setPWM(nServo , 0, pos);

}

void beginServos() {

  pwm.begin();
  pwm.setPWMFreq(frequencia);

}

// Atualiza, no índice específico da lista, os valores do encoder selecionado
void encoderUpdate(int clk, int dt, int index, float increment){

    atualCLK = digitalRead(clk);
    DT = digitalRead(dt);
    if(atualCLK != anterioresCLK[index]){
      if(atualCLK != DT){
        posDedo[index] -= increment;
      }
      else{
        posDedo[index] += increment;
      }
    }
    anterioresCLK[index] = atualCLK;
    delay(3);

}