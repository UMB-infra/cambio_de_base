from machine import Pin,ADC,I2C,PWM
from ssd1306 import SSD1306_I2C
import time, fb

# configuracion pantalla
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(23))
oled = SSD1306_I2C(ancho, alto, i2c)

#configuracion joistyck
ejey=ADC(Pin(35))
ejex=ADC(Pin(32))
ejey.atten(ADC.ATTN_11DB)   # para calibrar de 0 a 3.3v
ejey.width(ADC.WIDTH_12BIT) # establecer resolución
ejex.atten(ADC.ATTN_11DB)   # para calibrar de 0 a 3.3v
ejex.width(ADC.WIDTH_12BIT) # establecer resolución
boton=Pin(4,Pin.IN, Pin.PULL_UP)

def men_num(base):
    #variables iniciales
        posi = 0
        i = 0
        while True:
            #dibujo del menu
            x = ejex.read()
            y = ejey.read()
            oled.fill(1)
            oled.text(str(i),32,32,0)
            oled.vline(64,0,64,0)
            oled.text("limpiar",70,32,0)
            if posi == 0 :
                oled.hline(1,1,64,0)
                oled.hline(64,1,128,1)
                # envio el del numero
                if boton.value() == 0:
                    print(f"enviado{i}")
                    time.sleep(0.3)
                    return(i)
                #cambio del numero
                if y == 0 and i < base:
                    i += 1
                    time.sleep(0.1)
                elif y == 4095 and i > 0:
                    i  -= 1
                    time.sleep(0.1)
            
            # limpia el numero respecto al estado del menu
            elif posi == 1:
                oled.hline(1,1,64,1)
                oled.hline(64,1,128,0)
                if boton.value() == 0:
                    print("limpiar")
                    time.sleep(0.3)
                    i = 0
                    continue
            
            #cambio del numero respecto al estado del menu
            if posi == 0 and x == 4095:
                posi += 1
                print(posi)
            elif posi == 1 and x == 0:
                posi -= 1
                print(posi)
            oled.show()

def comp(num1):
    num = ''
    
    #ciclo para adjuntar los datos de la lista
    for i in num1:
        num += str(i)
    
    #seleccion si es numerico o string
    try:
        return(int(num))
    except:
        return(num)

def b10_bn(data,b):
    #conversion de base 10 a base n
    safe = data
    new = []
    new1 = []
    while safe >= b:
        new.append(safe % b)
        safe = safe // b
    new.append(safe)
    
    #ciclo de recolocacion de los datos
    for i in range(-1, -(len(new)+1), -1):
        new1.append(str(new[i]))
    
    if b > 10:
        #transformacion de numeros a letras
        new1 = reset(new1)
    
    #remplazo de lista a un dato unico
    new = comp(new1)
    return(new)

def bn_b10(data,b):
    #funcion de base n a base 10
    new = 0
    #ciclo de conversion a la inversa de la lista
    for i in range(-1, -(len(data) + 1), -1):
        exp = b ** -(i + 1)
        new += int(data[i]) * exp
    
    return(new)

def reset(num):
    num1 = []
    #ciclo para el cambio de numeros a letras
    for i in num:
        if i == '10':
            num1.append('A')
        elif i == '11':
            num1.append('B')
        elif i == '12':
            num1.append('C')
        elif i == '13':
            num1.append('D')
        elif i == '14':
            num1.append('E')
        elif i == '15':
            num1.append('F')
        else:
            num1.append(i)
    
    return(num1)

while True:
    f = None 
    num_i = []
    oled.text("programa pa cambiar bases",0,0,1)
    oled.show()
    time.sleep(0.5)
    #toma de base inicial
    oled.fill(0)
    oled.text("base inicial",0,0,1)
    oled.show()
    time.sleep(1)
    b_i = men_num(16)
    if b_i == 0:
        continue
    oled.fill(0)
    oled.text("cantidad de digitos",0,0,1)
    oled.show()
    time.sleep(1)
    #toma de cantidad de digitos
    c_d = men_num(50)
    if c_d == 0:
        continue
    #toma de numero segun la cantidad de digitos
    for i in range(c_d):
        oled.fill(0)
        oled.text(f"digi{i+1}",0,0,1)
        oled.show()
        time.sleep(0.4)
        num_i.append(men_num(b_i-1))
    #saca el numero de la lista
    
    print(num_i)
    #toma base final
    oled.fill(0)
    oled.text("base final",0,0,1)
    oled.show()
    time.sleep(1)
    b_f = men_num(16)
    if b_f == 0:
        continue
    if b_i != 10:
        if b_f != 10:
            data = bn_b10(num_i,b_i)
            data = b10_bn(data,b_f)
        else:
            data = bn_b10(num_i,b_i)
    else:
        num_i = comp(num_i)
        data = b10_bn(num_i,b_f)
          
    print(data)
    try:
        c = str(comp(num_i))
    except:
        c = str(num_i)
    oled.fill(1)
    oled.text(f"numero inicial de base {b_i}",0,0,0)
    oled.text(c,0,10,0)
    oled.text(f"numero inicial de base {b_f}",0,20,0)
    oled.text(str(data),0,30,0)
    oled.show()
    time.sleep(3)
    