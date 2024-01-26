using System;
using System.Globalization;
using System.Collections;

class Message
{
    public string timestamp {private set; get;} = "";
    public string arrivedTimestamp {private set; get;} = "";
    public Dictionary<char,int> pistao {private set; get;} = new Dictionary<char, int>();
    public double[] posicao  {private set; get;} = new double[3];
    public double abertura {private set; get;}
    private string Tipo;

    public Message(string ts, string dado, string tipo)
    {
        //Inserindo timestamp do instante que recebeu
        DateTime now = DateTime.Now;
        arrivedTimestamp = now.ToString("yyyy-MM-dd_HH:mm:ss:fff");

        //Inserindo timestamp enviada na mensagem
        timestamp = ts;

        //pricessando a mensagem pelo tipo dela
        if(tipo == "PISTAO")
        {
            pistaoProcessa(dado);
        }
        if(tipo == "POSICAO")
        {
            posicaoProcessa(dado);
        }
        if(tipo == "ABERTURA")
        {
            aberturaProcessa(dado);
        }
        Tipo = tipo;
    }

    private void posicaoProcessa(string coord)
    {
        //transforma os numeros de string para double salva no vetor de posições
        string[] posicoes = coord.Split(',');
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.NumberDecimalSeparator = ".";

        for(int i=0; i<3; i++)
        {
            posicao[i] =  Convert.ToDouble(posicoes[i], provider);
        }
    }

    private void pistaoProcessa(string pist)
    {
        //analise as possibilidades do pistão e retorna qual situação ele está
        for(int i = 0; i<pist.Length; i+=3)
        {
            int situacao = 4;  // 4 -> erro         
            if(pist[1+i] == '1' && pist[2+i] == '0') situacao = 1; // parado inicio
            if(pist[1+i] == '0' && pist[2+i] == '0') situacao = 2; // em movimento
            if(pist[1+i] == '0' && pist[2+i] == '1') situacao = 3; // parado final

            pistao.Add( ((char)('A'+ i/3)) , situacao);
        }
    }

    private void aberturaProcessa(string abert)
    {
        //transforma os numeros de string para double salva no vetor de posições
        NumberFormatInfo provider = new NumberFormatInfo();
        provider.NumberDecimalSeparator = ".";

        abertura =  Convert.ToDouble(abert, provider);
    }

    public override string ToString()
    {
        // cria a string que será passada no método Console.WriteLine
        if(Tipo == "PISTAO")
        {
            string pistaoString ="";
            foreach (KeyValuePair<char, int> item in pistao)
            {
                pistaoString += $"{item.Key}{item.Value},";
            }
            return $"S={timestamp} A={arrivedTimestamp}-> {pistaoString}";
        }
        if(Tipo == "POSICAO")
        {
            return $"S={timestamp} A={arrivedTimestamp}-> x: {posicao[0]}, y: {posicao[1]}, z: {posicao[2]} ";
        }
        if(Tipo == "ABERTURA")
        {
            return $"S={timestamp} A={arrivedTimestamp}-> Garra em {abertura}%";
        }
        else{
            return $"Mensagem com erro";
        }


        
    }


}