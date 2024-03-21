//Precisa apertar 'boot' for fazer upload do código, na parte de 'connecting'
#include <Arduino.h>
#include <NTPClient.h>
#include "String.h"
#include "time.h"
#include "PubSubClient.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>



//Declara as portas de leitura [pull up interno]
int sensores[8] = {14,16,17,18,22,23,19,21}; //{pist A Ini, pist A Fim, pist B Ini, ...}
#define POT 34 //verificar se eh esse mesmo //Sensor do potenciometro
#define ON  32
#define OFF 33
#define LED 9

//Define informacoes da rede
#define WLAN_SSID      "CampusVitoria"
#define WLAN_PASS      ""

// Cria um WiFiClient class para utilizar no MQTT server.
WiFiClientSecure client;
//Cria uma instância para medição de tempo
WiFiUDP ntpUDP;
NTPClient ntp(ntpUDP);

//Define informacoes MQTT
#define SERVER      "dd6e8d1cc8524360a537e7db4e5924f8.s2.eu.hivemq.cloud"
#define SERVERPORT   8883 
#define user        "Esp32"
#define pass        "Digital10@"

static const char *root_ca PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d
emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
)EOF";

// Cria os clientes MQTT
PubSubClient mqtt(client);
unsigned long lastMsg = 0;

void reconnect();
unsigned long millisZero();
void wait(int ciclo, int num);
// função construtora de data
String getFormattedDate(NTPClient& ntp) {
  String formattedDate;

  // Get the current time from NTP
  unsigned long epochTime = ntp.getEpochTime();
  time_t epochTimeAsTimeT = static_cast<time_t>(epochTime);

  // Convert the epoch time to a time structure
  struct tm timeInfo;
  gmtime_r(&epochTimeAsTimeT, &timeInfo);

  // Extract day, month, and year from the time structure
  int dayOfMonth = timeInfo.tm_mday;
  int month = timeInfo.tm_mon + 1; // Month is 0-based, so we add 1
  int year = timeInfo.tm_year + 1900; // Year is since 1900

  // Format the day and month to always have two digits
  String formattedDay = (dayOfMonth < 10) ? "0" + String(dayOfMonth) : String(dayOfMonth);
  String formattedMonth = (month < 10) ? "0" + String(month) : String(month);

  // Construct the date string in "DD/MM/YYYY" format
  formattedDate = formattedDay + "/" + formattedMonth + "/" + String(year);

  return formattedDate;
}
//Variaveis
  int f = 3;                   // valor em hz
  unsigned long time_ini;      // tempo em ms que comecou o segundo no timestamp
  unsigned long refTime = 0;   // tempo de inicio do loop
  bool ativar = true;          // indica se vai rodar a transmissao
  /*int garraMin = 400;        //valor minimo de abertura da garra
  int garraMax = 4095;         //valor maximo de abertura da garra
*/

void setup() {
  //Iniciando  
  Serial.begin(19200);
  
  Serial.println("Inicio");
  
  /*pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  //wait(500,2);  
  */
    //Declarando pinos de leitura dos pistoes
    for(int i = 0; i<8; i++){
      pinMode(sensores[i],INPUT_PULLUP);
    }
      pinMode(POT, INPUT);
  
  // Conecta o Wifi na rede
    Serial.println(); Serial.println();
    Serial.print("Conectando em ");
    Serial.println(WLAN_SSID);

    WiFi.mode(WIFI_STA);
    WiFi.begin(WLAN_SSID, WLAN_PASS);  

    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println();

    Serial.println("WiFi connected");
    Serial.print("IP address: "); 
    Serial.println(WiFi.localIP());

  //Conecta servidor MQTT
    client.setCACert(root_ca);
    mqtt.setServer(SERVER, SERVERPORT);
    reconnect();
    delay(500);
  
  //Inicia NTP para adquirir data e hora
   ntp.begin();
   ntp.setTimeOffset(-10800);//corrige para fuso horário     
}
String hora,date, epoch;
String space = "%%";


void loop() {
  if( (millis() - refTime) > (1000/f) && ativar)  //Controle da taxa de leitura
  {
    refTime = millis(); //Atualiza tempo de referencia

    //Criacao da mensagem
      int valores[8];
      hora = ntp.getFormattedTime();
      epoch = ntp.getEpochTime();
      String formattedDate = getFormattedDate(ntp);
      String msg = "%%PISTAO%%";
      String msg2 = "%%GARRA%%"; 
      msg += formattedDate + hora + space;//pistoes
      msg2 += hora + space + formattedDate + space;
    //Adicionando leituras dos sensores dos pistoes
    
    for(int i = 0; i<8; i++)
    {
      valores[i] = digitalRead(sensores[i]); 
      if( (i%2) == 0 ){
        char pistao = 'A' + i/2;
        msg += pistao;
      } 
      msg += valores[i];
    }
    //Adicionando leitura da garra(potenciomentro)
    //float valor = (analogRead(POT) - garraMin) * 100 / (garraMax - garraMin);
    int valor = analogRead(POT);
    msg2 += String(valor);
    
    
    

    // Publishes messages to MQTT server
    if (!mqtt.connected()) reconnect();
    mqtt.loop();
    if (!mqtt.publish("pistao", msg.c_str())) Serial.println("Failed to publish");
    if (!mqtt.publish("garra", msg2.c_str())) Serial.println("Failed to publish");
  }
  ntp.update();
}

void reconnect() {
  //Rotina de conexao
  while (!mqtt.connected()) {
    Serial.print("Conectando ao broker MQTT...");
    String clientId = "Esp32";
    clientId += String(random(0xffff), HEX);

    if (mqtt.connect(clientId.c_str(), user, pass)) {
      Serial.println("conectado");

      mqtt.subscribe("topic", 0);   // inscricao no topico 'topic'
    } else {
      Serial.print("falha, rc=");
      Serial.print(mqtt.state());
      Serial.println(" tentando novamente em 5 segundos");
      wait(1000,5);
    }
  }
}

unsigned long millisZero()
{
  struct tm timeinfo;
  getLocalTime(&timeinfo);
  int time_old = timeinfo.tm_sec;
  do{ 
    getLocalTime(&timeinfo); 
  }while(time_old == timeinfo.tm_sec);// rotina para descobrir quando acaba o segundo
  
  return millis();  //retorna o tempo em que o segundo começou
}

void wait(int ciclo, int num) //ciclo -> tempo do ciclo, num -> numero de repeticoes, LED -> porta led
{  
  for(int i = 0; i < num; i++)
  {
    //digitalWrite(LED, HIGH);
    delay( int(ciclo/2) );
    //digitalWrite(LED, LOW);
    delay( int(ciclo/2) );
  }
}
