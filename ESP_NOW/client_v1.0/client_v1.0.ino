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
      [X] No client colocar MAC do server
      [] No server colocar MAC do client

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

// Includes:
#include <esp_now.h>
#include <WiFi.h>

uint8_t broadcastAddress[] = {0xF4, 0x65, 0x0B, 0x56, 0xBE, 0x84};

char ultimoEstadoBotao = LOW;

typedef struct mensagem{
  char idServo[12];
  char acao[32];
  char valor;
} mensagem;

mensagem minhaMensagem;

esp_now_peer_info_t peerInfo;

void OnDataSent(const esp_now_send_info_t *tx_info, esp_now_send_status_t status){
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Succes": "Delivery Failed");
}

void enviarMensagem(){
  memset(&minhaMensagem, 0, sizeof(minhaMensagem));

  if(digitalRead(2)){
    strcpy(minhaMensagem.acao, "acendeLED");
  }else{
    strcpy(minhaMensagem.acao, "apagaLED");
  }

  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &minhaMensagem, sizeof(minhaMensagem));
  if (result == ESP_OK) {
    Serial.printf("Comando '%s' enviado.\n", minhaMensagem.acao);
  } else {
    Serial.println("Erro ao enviar a mensagem.");
  }
}

void setup(){
  Serial.begin(115200);

  pinMode(2, INPUT_PULLDOWN);

  WiFi.mode(WIFI_STA);

  if(esp_now_init() != ESP_OK){
    Serial.print("Error Initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);

  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if(esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }else{
    Serial.println("Peer added");
  }
}

void loop(){
  char estadoAtualBotao = digitalRead(2);

  if(estadoAtualBotao != ultimoEstadoBotao){
    delay(50);
    if(estadoAtualBotao == digitalRead(2)){
      enviarMensagem();
      ultimoEstadoBotao = estadoAtualBotao;
    }
  }
}

