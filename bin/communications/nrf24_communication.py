import time
import os
from pyrf24.rf24 import *
import queue  # Добавлен импорт модуля queue

ce_pin = int(os.getenv("CE_PIN"))
csn_pin = int(os.getenv("CSN_PIN"))
radio = RF24(ce_pin, csn_pin)
radio.begin(ce_pin, csn_pin)
channel = int(os.getenv("NRF_CHANNEL"))
radio.setChannel(channel)
pipe = [bytes(os.getenv("PIPE_RX")), bytes(os.getenv("PIPE_TX"))]
payload_size = int(os.getenv("PAYLOAD_SIZE"))
radio.setPayloadSize(payload_size)

radio.openReadingPipe(1, pipe[1])
radio.startListening()


def main_comm_loop(input_queue, output_queue):
    while True:
        if not input_queue.empty():
            message_data = input_queue.get()
            radio.openWritingPipe(pipe[0])
            radio.write(bytes(message_data, 'utf-8'))
            print(f"Data sent: {message_data}")
            radio.openReadingPipe(1, pipe[1])
            radio.startListening()
            time.sleep(1)

        if radio.available():
            received_data = 0
            radio.read(received_data)
            print(f"Received: {received_data}")
            output_queue.put(received_data)
            time.sleep(1)

if __name__ == "__main__":

    main_comm_loop(input_queue, output_queue)
