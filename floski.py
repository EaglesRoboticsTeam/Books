import brickpi3
import RPi.GPIO as GPIO
from time import sleep

BP = brickpi3.BrickPi3()

color = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

#Deifine os sensores infravermelhos array
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

#função dos motores
def mover(port1, pw1, port2, pw2):
    BP.set_motor_power(port1, 0)
    BP.set_motor_power(port2, 0)
    sleep(0)
    BP.set_motor_power(port1, pw1)
    sleep(0)
    BP.set_motor_power(port2, pw2)

#Line Follower Loop
#1 preto preto
#2 ponta direita
#3 ponta esquerda
try:
    while True:
        try:
            #Variáveis dos sensores de cor, esqueda e direita respectivamente
            color_sensor1 = BP.get_sensor(BP.PORT_1)
            color_sensor2 = BP.get_sensor(BP.PORT_2)

            #Reseta os motores
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))

            if GPIO.input(IR1) == GPIO.HIGH:
                if GPIO.input(IR4) == GPIO.HIGH:
                    mover(BP.PORT_A, 0, BP.PORT_B, 0)#1
                    sleep(0.2)
                    mover(BP.PORT_A, -10, BP.PORT_B, -10)
                    sleep(0.2)
                    #Verifica verde
                    if color[color_sensor1] == "Green":
                        mover(BP.PORT_A, -75, BP.PORT_B, 100)#3
                        sleep(0.2)
                    elif color[color_sensor2] == "Green":
                        mover(BP.PORT_A, 100, BP.PORT_B, -75)#2
                        sleep(0.2)
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

        except brickpi3.SensorError as error:
            print(error)
except KeyboardInterrupt:
    BP.reset_all()
