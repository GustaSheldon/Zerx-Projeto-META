/*
TODO:

[X] Configuração inicial(comum em server e client)
  [X] Incluir bibliotecas necessárias
    [X] <esp_now.h>
    [X] <WiFi.h>
  [X] Definir estrutura de mensagem única(struct)
  [X] Descobrir endereços MAC
    [X] Do server
    [X] Do client
  [X] Definir endereço do "parceiro"(peer)
    [] No client colocar MAC do server
    [X] No server colocar MAC do client

[X] Código de comunicação
  [X] Criar funções de callback
    [X] onDataSent
    [X] onDataRecv
  [X] No setup, inicializar WiFi, ESP-NOW, registrar callbacks e registrar o Peer
    [X] WiFi: "WiFi.mode(WIFI_STA);"
    [X] ESP-NOW: "if(esp-now-init != ESP_OK{Serial.println("Erro ao inicializar ESP-NOW"); return;})"
    [X] OnDataSent: "esp_now_register_send_cb(onDataSent);"
    [X] OnDataRcv: "esp_now_register_recv_cb(onDataRecv);"
    [X] Peer: "esp_now_peer_info_t peerInfo; memcpy(peerInfo.peer_addr, enderecoPeer, 6); peerInfo.channel = 0;  peerInfo.encrypt = false;"

[] Lógica de envio ou recepção(específica por ESP)
  [] Preencher structs com dados
  [] Enviar
*/

/* 
Endereços MAC do server e do client:

Server/Mestre: f4:65:0b:56:be:84
Client/Escravo: f4:65:0b:e7:32:38
*/

// Includes de bibliotecas
#include <esp_now.h>
#include <WiFi.h>

typedef struct mensagem{
  char idServo[12];
  char acao[32];
  char valor;
} mensagem;

mensagem minhaMensagem;

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len){
  memcpy(&minhaMensagem, incomingData, sizeof(minhaMensagem));
  if(strcmp(minhaMensagem.acao, "acendeLED") == 0 || strcmp(minhaMensagem.acao, "apagaLED") == 0){
    lidaLED(minhaMensagem);;
  }
}

void lidaLED(mensagem comando){
  if(strcmp(comando.acao, "acendeLED") == 0){
    Serial.println(">>> Comando recebido: ACENDER LED");
    digitalWrite(2, HIGH);
  }else if(strcmp(comando.acao, "apagaLED") == 0){
    Serial.println(">>> Comando recebido: APAGAR LED");
    digitalWrite(2, LOW);
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(2, OUTPUT);

  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}

void loop() {

}
