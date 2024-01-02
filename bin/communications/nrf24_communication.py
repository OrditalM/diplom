import time
from nrf24 import NRF24

# Настройки пинов CE и CSN
ce_pin = 25
csn_pin = 8

radio = NRF24()
radio.begin(0, 0, ce_pin, csn_pin)

channel = 0
radio.setChannel(channel)

# Устанавливаем адреса передатчика и приемника
pipe = [0xF0F0F0F0E1, 0xF0F0F0F0D2]

# Устанавливаем размер данных, который мы будем отправлять
payload_size = 32
radio.setPayloadSize(payload_size)

# Включаем режим приема
radio.openReadingPipe(1, pipe[1])
radio.startListening()

while True:
    # Проверяем, есть ли данные для чтения
    if radio.available():
        # Читаем данные
        received_data = []
        radio.read(received_data, radio.getDynamicPayloadSize())
        print(f"Received: {received_data}")

        # Включаем режим отправки
        radio.openWritingPipe(pipe[0])

        # Отправляем подтверждение
        radio.write("ACK")
        print("ACK sent")

        # Возвращаемся в режим приема
        radio.openReadingPipe(1, pipe[1])
        radio.startListening()

    time.sleep(1)
