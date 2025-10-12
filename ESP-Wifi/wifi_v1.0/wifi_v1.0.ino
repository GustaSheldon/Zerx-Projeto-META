/* 
TODO:

[X] Conectar-se ao Servidor Python
    [X] Incluir as bibliotecas WiFi, WebSocketsClient e ArduinoJson
    [X] Definir as credenciais do Wi-Fi (SSID, password)
    [X] No setup(), conectar-se à rede Wi-Fi
    [X] Iniciar a conexão WebSocket para o IP e porta do servidor Python
    [X] Registrar a função webSocketEvent para lidar com a comunicação
    [X] Dentro do onConnect do webSocketEvent, enviar uma mensagem JSON para o servidor para se identificar (ex.: {"tipo": "conexao", "id": "esp32"})

[] Receber e Enviar Informações
    [X] Na função webSocketEvent, no caso WStype_TEXT, usar deserializeJson() para analisar o comando do servidor
    [] Usar a lógica (if/else) para executar a ação dos servos com base no comando recebido
    [] Criar uma função, como enviarDadosDoSensor(), que será chamada no loop() do Arduino
    [] Dentro dela, criar um objeto JSON com os dados e usar webSocket.sendTXT() para enviá-lo de volta ao servidor
*/

// Includes:
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>

WebSocketsClient webSocket;

const char *ssid = "Blink_2G";
const char *password = "blink1020";
const char *webSocketServerIP = "192.168.18.202";
const uint16_t webSocketServerPort = 8001;

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length){

  switch(type){
    case WStype_DISCONNECTED:
      Serial.print("WebSocket desconectado");
      break;

    case WStype_CONNECTED:
      Serial.printf("Websocket conectado a: %s\n", payload);

      webSocket.sendTXT("{ \"tipo\":\"conexao\", \"id\":\"esp32\"}");
      break;

    case WStype_TEXT:
      Serial.printf("Texto recebido: %s\n", payload);

      StaticJsonDocument<256> doc;
      
      DeserializationError error = deserializeJson(doc, payload, length);

      if(error){
        Serial.print(("Falha no deserializeJson(): "));
        Serial.println(error.f_str());
        return;
      }

      const char *acao = NULL;
      if(doc["acao"].is<const char*>()){
        acao = doc["acao"];
        Serial.printf("Acao = %s\n\n\n", acao);
      }

      if(strcmp(acao, "moverServo") == 0){
        Serial.println("Tenho o moverServo");
        int servoId = 0;
        int angulo = 0;

        if(doc["dado"].is<JsonObject>()){
          JsonObject payloadObject = doc["dado"].as<JsonObject>();
          Serial.println("Objeto 'dado' encontrado");

          if (payloadObject["servo"].is<int>()) {
            servoId = payloadObject["servo"];
          }
          if(payloadObject["angulo"].is<int>()){
            angulo = payloadObject["angulo"];
          }
        }

        trataServos(servoId, angulo);
      }else if(strcmp(acao, "debugSensor") == 0){
        int sensorId = 0;

        Serial.println("Leu o debug na mensagem");

        if(doc["dado"].is<JsonObject>()){
          JsonObject payloadObject = doc["dado"].as<JsonObject>();
          Serial.println("Objeto 'dado' encontrado");

          if (payloadObject["sensorId"].is<int>()) {
            sensorId = payloadObject["sensorId"];
          }
        }

        enviaDadosSensor(sensorId);
      }

      break;
  }
}

void trataServos(int servoId, int angulo){
  Serial.printf("Id do servo = %d, valor do angulo = %d\n\n\n", servoId, angulo);
}

void enviaDadosSensor(int sensorId){
  Serial.printf("Pediu informações do sensor: %d\n\n\n", sensorId);
}

void setup() {
  
  Serial.begin(115200);

  Serial.println();
  Serial.print("Conectando a: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());

  webSocket.begin(webSocketServerIP, webSocketServerPort, "/");
  webSocket.onEvent(webSocketEvent);

}

void loop() {
  
  webSocket.loop();

}
