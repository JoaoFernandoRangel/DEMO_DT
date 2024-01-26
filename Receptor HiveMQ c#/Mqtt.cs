using System;
using System.Text;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System.Security.Cryptography.X509Certificates;
/*
Para instalar o pacote, executar no terminal:
    dotnet add package M2Mqtt --version 4.3.0
*/

class Mqtt
{
    //DADOS DE CONEXÃO COM O SERVIDOR
        public string user {private set; get;}
        public string pass {private set; get;}
        public string server {private set; get;}
        public int port {private set; get;}
        public string topic {private set; get;}
        public MqttClient client {private set; get;}
    
    //VARIÁVEIS DE FUNCIONAMENTO
        public bool msgToReadPis {private set; get;} //Retorna se há mensagens não "lidas" do pistao
        public bool msgToReadPos {private set; get;} //Retorna se há mensagens não "lidas" da posicao
        public bool msgToReadAber {private set; get;} //Retorna se há mensagens não "lidas" da abertura da garra

            //Lista que armazena as mensagens do pistão
        private List<Message> Pistao = new();
        public List<Message> pistao
        {
            get{
                msgToReadPis = false;
                return Pistao;
            }     
        }

            //Lista que armazena as mensagens de posicao
        private List<Message> Posicao = new();
        public List<Message> posicao
        {
            get{
                msgToReadPos = false;
                return Posicao;
            }     
        }

            //Lista que armazena as mensagens de abertura da garra
        private List<Message> Abertura = new();
        public List<Message> abertura
        {
            get{
                msgToReadAber = false;
                return Abertura;
            }     
        }

//######################################################################################################

    //MÉTODOS DA CLASSE
    public Mqtt(string tpc = "topic", int prt = 8883, string usr = "DigitalTwin", string pss = "Digital7w1n", string svr = "be7ffc1c90054731998da6666ee7b112.s2.eu.hivemq.cloud")
    {
        // Adicionando as credenciais nas variáveis
        user = usr; pass = pss; server = svr; port = prt; topic = tpc;

        // criar uma nova instância do cliente MQTT
        X509Certificate caCert = X509Certificate.CreateFromCertFile("isrgrootx1.pem");        
        client = new MqttClient(server, port, true, caCert, null, MqttSslProtocols.TLSv1_2);
        client.MqttMsgPublishReceived += client_MqttMsgPublishReceived; // manipulador para o recebimento de mensagens

        Conectar();                
    }
 
    public void Conectar(){
        // conectar ao broker MQTT e ao tópico
        int retries = 0;
        while(!client.IsConnected)
        {
            client.Connect("Terminal", user, pass);
            retries++;

            if (retries>10){
                Console.WriteLine("Erro De Conexão");
                break;
            }     
        }

        client.Subscribe(new string[] { topic }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE } );
        Console.WriteLine("Conectado ao tópico.");
    }

    private void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {
        // mensagem recebida    
        string[] msg = Encoding.UTF8.GetString(e.Message).Split("%%");

        if(msg.Length == 5) {
            if( msg[1] == "PISTAO"){
                pistao.Add( new Message(msg[2], msg[3], "PISTAO") ); 
                msgToReadPis = true;
            }
            if( msg[1] == "POSICAO"){
                posicao.Add( new Message(msg[2], msg[3], "POSICAO") );
                msgToReadPos = true;
            }
            if( msg[1] == "ABERTURA"){
                abertura.Add( new Message(msg[2], msg[3], "ABERTURA") );
                msgToReadAber = true;
            }
        }
    }
}
