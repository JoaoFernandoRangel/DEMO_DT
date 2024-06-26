import time
from time import sleep
from datetime import datetime
import os
import math


rotina = 4 #mudar dependendo da rotina a ser executada
pc = "jf" #deixar igual a jf quando no notebook, mudar para outro valor quando no pc do 204


#rotina 1 = mover o robo com a mão e fazer a Unity copiar
#rotina 2 = rotina pré programada de movimentação com abertura e fechamento de garra
#rotina 3 = movimentação do braço com pistões
#rotina 4 = simulação de falha com o potênciometro
#rotina 5 = acionamento do ciclo de 1 peça



string_garra = "GA"
space = "%%"

###########################################
###########################################

if (pc=="jf"):
    diretorio = "C:\\Users\\João Fernando Rangel\\Desktop\\Digital Twin\\DEMO_DT\\Position_tracker\\Logs\\log"
else:
    diretorio = "C://Users//Digital Twin//Documents//GitHub//DEMO_DT//Position_tracker//Logs//log"
data_hora_atual = datetime.now()
formato_data_hora = "%Y-%m-%d_%H-%M-%S"
timestamp = data_hora_atual.strftime(formato_data_hora)
diretorio_novo =  diretorio.replace("log", "") + "Logs%%" + timestamp + ".txt"
log = open(diretorio_novo, 'w+')

def current_milli_time():
    return round(time.time() * 1000)


def configura():
	global aprox
	aprox = 30
	dType.SetIOMultiplexingEx(api, 19, 3, 1)
	dType.SetIOMultiplexingEx(api, 20, 3, 1)
	dType.SetIOMultiplexingEx(api, 7, 3, 1)
	dType.SetIOMultiplexingEx(api, 4, 3, 1)
	dType.SetIOMultiplexingEx(api, 5, 3, 1)
	dType.SetIOMultiplexingEx(api, 18, 1, 1)#Pistão A
	dType.SetIOMultiplexingEx(api, 14, 1, 1)#Pistao B
	dType.SetIOMultiplexingEx(api, 15, 1, 1)#Pistão C
	dType.SetIOMultiplexingEx(api, 6, 1, 1)#Pistão D
	dType.SetIOMultiplexingEx(api, 13, 1, 1)#Motor vertical
	dType.SetIOMultiplexingEx(api, 17, 1, 1)#Esteira 1
	dType.SetIOMultiplexingEx(api, 2, 1, 1)#Esteira 2
	dType.SetIOMultiplexingEx(api, 13, 1, 1)

def update(): 
    #log = open(diretorio_novo, 'w+')
    global string_garra
    #string_garra = "GF"
    pose_info_atual = dType.GetPose(api)  # Supondo que dType.GetPose(api) é uma função válida
    # Verifique se houve uma mudança na pose_info
    data_hora_atual = datetime.now()
    formato_data_hora = "%H-%M-%S"
    timestamp1 = data_hora_atual.strftime(formato_data_hora)
    string = str(round(pose_info_atual[0], 3)) + space + str(round(pose_info_atual[1], 3)) + space + str(
        round(pose_info_atual[2], 3)) + space + str(round(pose_info_atual[3], 3)) + space + string_garra
    string_Print = str(timestamp1) + space + string  + "\n"
    log.write(string_Print + "\n")
    print('Posição escrita no registro de atividades') 
    epoch = current_milli_time()   
    # Crie um novo arquivo com o nome baseado na string escrita e na hora de criação
    novo_arquivo = diretorio + space + str(epoch) + space + timestamp1 + space+ string  + space + ".txt" #+ space +str(epoch)
    with open(novo_arquivo, "w+") as x:
        x.write(string_Print)
        print('Novo arquivo criado')
    # Atualize a pose_info_anterior
    #log.close()
    time.sleep(0.5)


jump_param = 50 # altura para movimento tipo jump
ponto_esteira = [110.5752, -173.1466, 33.9814, -93.6851]
home = [223.0752, 2.4736, 67.9859, 0]
montagem = [287.5588 , 3.0321 , 38.6762 , 10.6513]
montagemtampa = [287.0620 , 2.6663 , 56.7805 , 7.4995]
tampa1 = [190.5303 , 72.3327 , 23.4604 , 8.6788]
peca1 = [188.3365 , 178.3896 , 36.2875 , -35.9722]

azul1 = [-81.6309 , -165.2486 , 24.5483 , -90]
vermelha1 = [-14.8509 , -165.2496, 26.1557, -128.3200]
insere = [286.3870 ,1.4466, 67.1643 , -11.7400]
retirapronta = [286.3913 , 2.6706 , 34.3566 , -78.5320]
#ponto_descarte = [146.3089,-105.9902,41.5474,-81.4603] #ponto para soltar o copo fora da área de trabalho.
ponto_descarte = [286.3870 ,1.4466, 87.1643 , -11.7400] #ponto para soltar o copo fora da área de trabalho.
#ponto_pega = [0,0,0,0]
ponto_pega = montagem

def funcao_descarte():
    update()
    #Adicionar pontos intermediários
    #dType.SetPTPCmdEx(api,0,(ponto_descarte[0]),(ponto_descarte[1]),(ponto_descarte[2]),(ponto_descarte[3]),1)
    jump(ponto_descarte) 
    update()
    abregarra()
    update()

def jump(ponto): #função que substitui o modo jump.
    global jump_param
    pose_atual = dType.GetPose(api)
    update()
    dType.SetPTPCmdEx(api, 1, (pose_atual[0]), (pose_atual[1]), jump_param, (pose_atual[3]), 1)
    update()
    dType.SetPTPCmdEx(api, 1, (ponto[0]), (ponto[1]), jump_param, (ponto[3]), 1)
    update()
    dType.SetPTPCmdEx(api, 1, (ponto[0]), (ponto[1]), (ponto[2]), (ponto[3]), 1)
    update()

def pega_ponto(ponto):
    update()
    #dType.SetPTPCmdEx(api, 0, (ponto[0]), (ponto[1]), (ponto[2] + aprox), (ponto[3]), 1)
    jump(ponto) # função própria de movimentação tipo jump
    update()
    dType.SetPTPCommonParamsEx(api, 5, 5, 1) # altera os parametros de vel e aceleração
    update()
    abregarra()
    dType.SetPTPCmdEx(api, 1, (ponto[0]), (ponto[1]), (ponto[2]), (ponto[3]), 1) # vai até o ponto fornecido
    update()
    #dType.SetPTPCommonParams(api, velocityRatio, accelerationRatio, isQueued=0)
    fechagarra()
    update()
    dType.SetPTPCmdEx(api, 1, (ponto[0]), (ponto[1]), (ponto[2] + aprox), (ponto[3]), 1) # sobre um valor fixo do ponto fornecido
    update()


def pegaesteira():
    update()
    #dType.SetPTPCmdEx(api,0,(ponto_esteira[0]),(ponto_esteira[1]),(ponto_esteira[2] + aprox),(ponto_esteira[3]),1)
    jump(ponto_esteira)
    update()
    dType.SetPTPCommonParamsEx(api,5,5,1)
    update()
    dType.SetPTPCmdEx(api,1,(ponto_esteira[0]),(ponto_esteira[1]),(ponto_esteira[2]),(ponto_esteira[3]),1)
    update()
    #dType.SetPTPCommonParams(api, velocityRatio, accelerationRatio, isQueued=0)
    fechagarra()
    update()
    dType.SetPTPCmdEx(api,1,(ponto_esteira[0]),(ponto_esteira[1]),(ponto_esteira[2] + aprox),(ponto_esteira[3]),1)
    update()

def abregarra():
    global string_garra
    dType.SetWAITCmdEx(api, 500, 1)
    dType.SetEndEffectorGripperEx(api, 1, 0)
    dType.SetWAITCmdEx(api, 500, 1)
    string_garra = "GA"

def fechagarra():
    global string_garra
    dType.SetWAITCmdEx(api, 500, 1)
    dType.SetEndEffectorGripperEx(api, 1, 1)
    dType.SetWAITCmdEx(api, 500 ,  1)
    string_garra = "GF"

def rotina1(vezes, escolha):
    if escolha == 0:
        for i in range(vezes):
            if (i%20 == 0):
                fechagarra()
            else:
                abregarra()
            update()
    else:
        while (True):
            update()


def rotina2(): #Faz uma forma geometrica simples e abre e fecha a garra
    dType.SetPTPCommonParamsEx(api,25,25,1)
    update()	
    abregarra()
    update()
    dType.SetPTPCmdEx(api,1,home[0],home[1],home[2],home[3],1) #Home
    update()
    for count in range(1):
        dType.SetPTPCmdEx(api,1,home[0],(home[1]-60),(home[2]+50),(home[3]+60),1) #Vertice A
        update()
        fechagarra()
        update()
        dType.SetPTPCmdEx(api,1,home[0],(home[1]-60),(home[2]-20),(home[3]-60),1) #Vértice B
        update()
        abregarra()
        update()
        dType.SetPTPCmdEx(api,1,home[0],(home[1]+120),(home[2]-20),(home[3]+60),1) #Vértice C
        update()
        fechagarra()
        update()
        dType.SetPTPCmdEx(api,1,home[0],(home[1]+120),(home[2]+50),home[3],1) #Vértice D
        update()
    abregarra()
    update()
    dType.SetPTPCmdEx(api,1,home[0],home[1],home[2],home[3],1) #Home
    update()

def move_para_ponto(ponto_num,ponto_id):
    if (ponto_id == "1"):
        update()
        dType.SetPTPCmdEx(api,1,ponto_num[0],(ponto_num[1]),(ponto_num[2]),ponto_num[3],1) #Home
        update()   
    elif (ponto_id == "A"):
        update()
        dType.SetPTPCmdEx(api,1,ponto_num[0],(ponto_num[1]-60),(ponto_num[2]+50),ponto_num[3]+60,1) #Vértice A
        update()
    elif (ponto_id == "B"):
        update()
        dType.SetPTPCmdEx(api,1,ponto_num[0],(ponto_num[1]-60),(ponto_num[2]-20),(ponto_num[3]-60),1) #Vértice B
        update()
    elif (ponto_id == "C"):
        update()
        dType.SetPTPCmdEx(api,1,ponto_num[0],(ponto_num[1]+120),(ponto_num[2]-20),(ponto_num[3]+60),1) #Vértice C
        update()
    elif (ponto_id == "D"):
        update()
        dType.SetPTPCmdEx(api,1,ponto_num[0],(ponto_num[1]+120),(ponto_num[2]+50),ponto_num[3],1) #Vértice D
        update()


def rotina3(vezes):
    print("Iniciando rotina 3")
    configura()
    time.sleep(5)
    move_para_ponto(home, "1")
    for i in range(vezes):
        dType.SetIODOEx(api, 18, 1, 1) #Envia o pistão A
        move_para_ponto(home, "A")
        dType.SetIODOEx(api, 14, 1, 1) #Envia o pistão B
        move_para_ponto(home, "B")
        dType.SetIODOEx(api, 15, 0, 1) #Retorna o pistão C
        move_para_ponto(home, "C")
        dType.SetIODOEx(api, 6, 1, 1) #Envia o pistão D
        move_para_ponto(home, "D")
        time.sleep(3)
        move_para_ponto(home, "A")
        dType.SetIODOEx(api, 14, 0, 1) #Retorna o pistão B
        move_para_ponto(home, "C")
        dType.SetIODOEx(api, 15, 1, 1) #Avança o pistão C
        move_para_ponto(home, "B")
        time.sleep(3)
        move_para_ponto(home, "D")
        dType.SetIODOEx(api, 18, 0, 1) #Retorna o pistão A
        move_para_ponto(home, "A")
        dType.SetIODOEx(api, 14, 0, 1) #Retorna o pistão B
        move_para_ponto(home, "B")
        dType.SetIODOEx(api, 15, 0, 1) #Retorna o pistão C
        move_para_ponto(home, "D")
        dType.SetIODOEx(api, 6, 0, 1) #Retorna o pistão D
        move_para_ponto(home, "C")
        time.sleep(3)
        move_para_ponto(home, "A")
        dType.SetIODOEx(api, 18, 1, 1) #Avança o pistão A
        dType.SetIODOEx(api, 14, 1, 1) #Avança o pistão B
        dType.SetIODOEx(api, 6, 1, 1) #Retorna o pistão D
        move_para_ponto(home, "B")
        time.sleep(3)
        move_para_ponto(home, "C")
        dType.SetIODOEx(api, 18, 0, 1) #Retorna o pistão A
        move_para_ponto(home, "D")
        time.sleep(3)
        move_para_ponto(home, "A")
        dType.SetIODOEx(api, 18, 1, 1) #Avança o pistão A
        move_para_ponto(home, "D")
        time.sleep(3)
        move_para_ponto(home, "B")
        dType.SetIODOEx(api, 14, 0, 1) #Retorna o pistão B
        move_para_ponto(home, "C")
        time.sleep(3)
        move_para_ponto(home, "D")
        dType.SetIODOEx(api, 15, 1, 1) #Avança o pistão C
        move_para_ponto(home, "A")
        time.sleep(3)
        move_para_ponto(home, "B")
        dType.SetIODOEx(api, 15, 0, 1) #Retorna o pistão C
        move_para_ponto(home, "C")
        time.sleep(3)
        move_para_ponto(home, "D")
        dType.SetIODOEx(api, 6, 1, 1) #Avança o pistão D
        move_para_ponto(home, "A")
        time.sleep(3)
        move_para_ponto(home, "D")
        dType.SetIODOEx(api, 6, 0, 1) #Retorna o pistão D
        move_para_ponto(home, "1")
        time.sleep(3)

def rotina4(vezes, ponto): #teste de captura de copo
    global home
    print("Rotina 4")
    time.sleep(3)
    dType.SetPTPCmdEx(api,1,home[0],home[1],home[2],home[3],1) #Home
    abregarra()

    for i in range(vezes):
        if (ponto == "esteira"):
            pegaesteira()
            time.sleep(3)
            funcao_descarte()
            time.sleep(3)
        else:
            pega_ponto(ponto_pega)
            time.sleep(3)
            funcao_descarte()
            time.sleep(3)
            

configura() #declara as funções para manipulação dos pistões
turnos = 200
if (rotina==0):
    print('rotina 0')
elif (rotina==1):
#rotina 1 = mover o robo com a mão e fazer a Unity copiar
    print('rotina 1')
    rotina1(turnos, 1) # mude para 0 para abilitar abertura e fechamento da garra
elif (rotina==2):
#rotina 2 = rotina pré programada de movimentação com abertura e fechamento de garra
    print('rotina 2')
    for count in range(1):
        rotina2()
elif (rotina==3):
#rotina 3 = movimentação do braço com pistões
    print('rotina 3')
    rotina3(5)    
elif (rotina==4):
#rotina 4 = simulação de falha com o potênciometro
    print('rotina 4')
    rotina4(5, "esteira")


log.close()