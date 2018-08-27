from datetime import datetime, timedelta
from time import sleep

tempo = timedelta(seconds=10)

while True:
    sleep(1)
    tempo = tempo - timedelta(seconds=1)
    print(tempo)
