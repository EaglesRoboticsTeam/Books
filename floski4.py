import brickpi3
import RPi.GPIO as GPIO
from time import sleep

BP = brickpi3.BrickPi3()

#Deifine os sensores infravermelhos do array numerados de acordo com os pinos físicos do RaspberryPi3
IR1 = 7
IR2 = 11
IR3 = 13
IR4 = 15
#Sensor RGB esquerdo
s2 = 23
s3 = 24
signal1 = 22
#Sensor RGB direito
s22 = 29
s23 = 31
signal2 = 32

NUM_CYCLES = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Define o tipo das portas do IR
GPIO.setup(IR1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Sensor RGB esquerdo
GPIO.setup(signal1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s2,GPIO.OUT)
GPIO.setup(s3,GPIO.OUT)
#Sesnor RGB direito
GPIO.setup(signal2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s22,GPIO.OUT)
GPIO.setup(s23,GPIO.OUT)

#Função dos motores
def mover(port1, pw1, port2, pw2):
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(port1))#sempre resetar os motores
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(port2))#sempre resetar os moteres
    BP.set_motor_power(port1, pw1)
    BP.set_motor_power(port2, pw2)

#Line Follower Loop
#1 Preto-Preto
#2 Ponta direita
#3 Ponta esquerda
    
try:
    while True:
        try:
            if GPIO.input(IR1) == GPIO.HIGH:
                if GPIO.input(IR4) == GPIO.HIGH: 
                    mover(BP.PORT_C, 0, BP.PORT_B, 0)
                    mover(BP.PORT_C, -20, BP.PORT_B, -20)
                    sleep(0.3)
                    
                    #Verifica verde
                    #RGB 1
                    GPIO.output(s2,GPIO.LOW)
                    GPIO.output(s3,GPIO.LOW)
                    sleep(0.3)
                    start = time()
                    for impulse_count in range(NUM_CYCLES):
                      GPIO.wait_for_edge(signal1, GPIO.FALLING)
                    duration = time() - start 
                    red1  = NUM_CYCLES / duration

                    #RGB 2
                    GPIO.output(s22,GPIO.LOW)
                    GPIO.output(s23,GPIO.LOW)
                    sleep(0.3)
                    start = time()
                    for impulse_count in range(NUM_CYCLES):
                      GPIO.wait_for_edge(signal2, GPIO.FALLING)
                    duration = time() - start 
                    red1  = NUM_CYCLES / duration
    
                    if 8000 < red1 < 11000:
                        if 8000 < red2 < 11000:
                            mover(BP.PORT_C, -100, BP.PORT_B, 100)
                            sleep(0.5)
                        else:
                            mover(BP.PORT_C, -75, BP.PORT_B, 100)
                            sleep(0.3)
                    elif 8000 < red2 < 11000:
                        if 8000 < red1 < 11000:
                            mover(BP.PORT_C, -100, BP.PORT_B, 100)
                            sleep(0.5)
                        else:
                            mover(BP.PORT_C, 100, BP.PORT_B, -75)
                            sleep(0.3)
                    else:
                        mover(BP.PORT_C, 100, BP.PORT_B, 100)
                        sleep(0.4)
                elif GPIO.input(IR4) == GPIO.LOW:
                    mover(BP.PORT_C, 100, BP.PORT_B, -75)#2

            elif GPIO.input(IR1) == GPIO.LOW:
                if GPIO.input(IR4) == GPIO.HIGH:
                    mover(BP.PORT_C, -75, BP.PORT_B, 100)#3

                elif GPIO.input(IR4) == GPIO.LOW:
                    if GPIO.input(IR2) == GPIO.HIGH:
                        if GPIO.input(IR3) == GPIO.LOW:
                            mover(BP.PORT_C, 100, BP.PORT_B, -90)

                    elif GPIO.input(IR2) == GPIO.LOW:
                        if GPIO.input(IR3) == GPIO.HIGH:
                            mover(BP.PORT_C, -90, BP.PORT_B, 100)
                        elif GPIO.input(IR3) == GPIO.LOW:
                            mover(BP.PORT_C, 40, BP.PORT_B, 40)

        except brickpi3.SensorError as error: #CASO O SENSOR DEMORE PARA INICIALIZAR O EXCEPT SERVE PARA DA TEMPO DE INICIAR O SENSSOR
            print(error)
except KeyboardInterrupt: #FECHANDO O PROGRAMA  
    BP.reset_all()
