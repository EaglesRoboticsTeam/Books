import brickpi3
import RPi.GPIO as GPIO
from time import sleep

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

#Deifine os sensores infravermelhos do array numerados de acordo com os pinos físicos do RaspberryPi3
IR1 = 7
IR2 = 11
IR3 = 13
IR4 = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Define o tipo das portas
GPIO.setup(IR1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Função dos motores
def mover(port1, pw1, port2, pw2):
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(port1))#sempre resetar os motores
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
                    
                    mover(BP.PORT_A, -20, BP.PORT_B, -20)
                    sleep(0.7)
                    mover(BP.PORT_A, 0, BP.PORT_B, 0)#1
                    sleep(0.9)
                    #Verifica verde
                    try:
                        color_sensor1 = BP.get_sensor(BP.PORT_1)
                        color_sensor2 = BP.get_sensor(BP.PORT_2)
                        
                        if color[color_sensor1] == "Green":
                            if color[color_sensor2] == "Green":
                                mover(BP.PORT_A, -100, BP.PORT_B, 100)
                                sleep(0.8)
                            else:
                                mover(BP.PORT_A, 100, BP.PORT_B, 100)#3
                                sleep(0.1)
                                mover(BP.PORT_A, -75, BP.PORT_B, 100)#3
                                sleep(0.4)
                        elif color[color_sensor2] == "Green":
                            if color[color_sensor1] == "Green":
                                mover(BP.PORT_A, -100, BP.PORT_B, 100)
                                sleep(0.8)
                            else: 
                                mover(BP.PORT_A, 100, BP.PORT_B, 100)#3
                                sleep(0.1)
                                mover(BP.PORT_A, 100, BP.PORT_B, -75)#3
                                sleep(0.4)
                        else:
                            mover(BP.PORT_A, 50, BP.PORT_B, 50)#3
                            sleep(0.3)
                    except brickpi3.SensorError as error:
                        print(error)
                elif GPIO.input(IR4) == GPIO.LOW:
                    mover(BP.PORT_A, 100, BP.PORT_B, -75)#2

            elif GPIO.input(IR1) == GPIO.LOW:
                if GPIO.input(IR4) == GPIO.HIGH:
                    mover(BP.PORT_A, -75, BP.PORT_B, 100)#3

                elif GPIO.input(IR4) == GPIO.LOW:
                    if GPIO.input(IR2) == GPIO.HIGH:
                        if GPIO.input(IR3) == GPIO.LOW:
                            mover(BP.PORT_A, 100, BP.PORT_B, -90)

                    elif GPIO.input(IR2) == GPIO.LOW:
                        if GPIO.input(IR3) == GPIO.HIGH:
                            mover(BP.PORT_A, -90, BP.PORT_B, 100)
                        elif GPIO.input(IR3) == GPIO.LOW:
                            mover(BP.PORT_A, 40, BP.PORT_B, 40)

        except brickpi3.SensorError as error: #CASO O SENSOR DEMORE PARA INICIALIZAR O EXCEPT SERVE PARA DA TEMPO DE INICIAR O SENSSOR
            print(error)
except KeyboardInterrupt: #FECHANDO O PROGRAMA
    BP.reset_all()
