# 🤖 Zerx-Projeto-META

  Projeto de mão robótica controlada por movimentos reais da mão de uma pessoa, interpretados usando encoders e um ESP32, que envia valores para o Arduino, através de comunicação bluetooth, para que servos sejam controlados em tempo real
  
## ℹ️ Sobre o projeto:
  Este projeto tem como objetivo o uso em fábricas e ambientes de trabalho que podem trazer perigos aos trabalhadores, para que um operário possa realizar seu trabalho através da mão robótica, não colocando seu membro em risco.
  Utilizando uma série de cordas presas a encoders, um ESP32 faz a leitura dos movimentos do usuário.
  Esses dados são então enviados, através de uma comunicação serial, para o Arduino, que os recebe e interpreta, para que possa controlar os servos de forma que repliquem os movimentos realizados pelo usuário
  
  Obs.: para programação do código do Arduino, foi usada a extensão PlatformIO do VsCode, não a ArduinoIDE
  
### ⚙️ Funcionalidades:
  - 📷 Rastreamento de movimentos da mão em tempo real com os encoders;
  - 📞 Comunicação bluetooth entre ESP32 e Arduino;
  - 🎮 Controle de servomotres para replicação dos movimentos captados;
  - 🔓 Sistema extensível para adicionar mais articulações e melhorias futuras

## 🔥 Projeto:

### Requisitos:
  - Python 3.x;
  - ESP32(ou similar)
  - 5 encoders
  - Arduino IDE(ou alternativa);
  - Arduino UNO(ou similiar);
  - Servomotores(5x para dedos, um por dedo)

### 🧩 Implementação:
  1. Clone este repositório:
      ```bash
     git clone https://github.com/GustaSheldon/Zerx-Projeto-META.git
     cd Zerx-Projeto-META
  2. Instale bibliotecas do Python:
     ```bash
     pip install opencv-python pyserial
  3. Abra e upe o código Arduino para seu microcontrolador
  4. Execute o script Python

### 🚀 Como usar:
  - Conecte os dois módulos(ESP32 com encoder + Arduino com servos) a qualquer fonte de energia.
  - Estabeleça a conxão bluetooth.
  - Veja os movimentos de um módulo serem replicados no outro em tempo real!

### 📓 Diário de bordo:
  ```bash
  https://docs.google.com/document/d/1PFmZ-JfQwFuOwu88TLG1hwXJkmD0gUxjG_UbMS_SyS4/edit?usp=sharing

testezinho
