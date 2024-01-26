using System;
using System.Text;


class Program
{
    static void Main(string[] args)
    {
        // Credenciais de conexão
        // string user = "DigitalTwin";
        // string pass = "Digital7w1n";
        // string server = "be7ffc1c90054731998da6666ee7b112.s2.eu.hivemq.cloud";
        // int port = 8883;

        Mqtt mqtt = new();
        Message mensagem;
        string lastPis = "";
        string lastPos = "";

        // aguardar mensagens indefinidamente
        while (true) {

            if(!mqtt.client.IsConnected){
                mqtt.Conectar();
            }                

            if( mqtt.pistao.Count > 0 )
            {
                mensagem = mqtt.pistao.Last();
                if (lastPis != $"{mqtt.pistao.Count} - {mensagem}"){               
                    lastPis = $"{mqtt.pistao.Count} - {mensagem}";       
                    Console.WriteLine(lastPis);
                }        
            }

            if( mqtt.posicao.Count > 0 )
            {
                mensagem = mqtt.posicao.Last();
                if (lastPos != $"{mqtt.posicao.Count} - {mensagem}"){               
                    lastPos = $"{mqtt.posicao.Count} - {mensagem}";       
                    Console.WriteLine(lastPos);
                }        
            }

            if( mqtt.abertura.Count > 0 )
            {
                mensagem = mqtt.abertura.Last();
                if (lastPos != $"{mqtt.abertura.Count} - {mensagem}"){               
                    lastPos = $"{mqtt.abertura.Count} - {mensagem}";       
                    Console.WriteLine(lastPos);
                }        
            }

            Thread.Sleep(10);
        }

    }
}