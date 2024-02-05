#Eixo Y
#70.5915    24.6074    xxxxxxxxxxxxxxx      -66,7842
#Eixo X
#184.1713   139,0746  xxxxxxxxxxxxxxx       51,907
#Eixo Z
#33,5399    46,7404                76,0925            

eixoy = [70.5915, 24.6074, 0, -66.7842] #indo para a esquerda
eixox =[184.1713,139.0746,0,51.907]
eixoz =[33.5399,46.7404,0,76.0925]

dif_y_1 = eixoy[1]-eixoy[0]
dif_y_2 = eixoy[3]-eixoy[1]
dif_y_3 = eixoy[3]-eixoy[0]
razao_y = dif_y_2/dif_y_1
razao_y_1 = dif_y_3/dif_y_1
print('eixo y')
print(dif_y_1)
print(dif_y_2)
print(razao_y)
print(razao_y_1)

print("#######################")
print('eixo x')
dif_x_1 = eixox[1]-eixox[0]
dif_x_2 = eixox[3]-eixox[1]
dif_x_3 = eixox[3]-eixox[0]
razao_x = dif_x_2/dif_x_1
razao_x_1 = dif_x_3/dif_x_1
print(dif_x_1)
print(dif_x_2)
print(razao_x)
print(razao_x_1)

print("#######################")
print('eixo z')
dif_z_1 = eixoz[1]-eixoz[0]
dif_z_2 = eixoz[3]-eixoz[1]
dif_z_3 = eixoz[3]-eixoz[0]
razao_z = dif_z_2/dif_z_1
razao_z_1 = dif_z_3/dif_z_1
print(dif_z_1)
print(dif_z_2)
print(razao_z)
print(razao_z_1)











#home = [223.0752, 2.4736, 67.9859, 0]
#dType.SetPTPCmdEx(api,1,(home[0]),(home[1]),(home[2]),(home[3]),1)