import time
import os
from nrf24 import NRF24

ce_pin = os.getenv("CE_PIN")
csn_pin = os.getenv("CSN_PIN")
radio = NRF24(ce_pin, csn_pin)
radio.begin(0, 0, ce_pin, csn_pin)
channel = os.getenv("NRF_CHANNEL")
radio.setChannel(channel)
pipe = [os.getenv("PIPE_RX"), os.getenv("PIPE_TX")]
payload_size = os.getenv("PAYLOAD_SIZE")
radio.setPayloadSize(payload_size)

radio.openReadingPipe(1, pipe[1])
radio.startListening()


def main_comm_loop(message_data=None):
    received_data = []
    while True:
        if radio.available():
            if not message_data is None:
                radio.openWritingPipe(pipe[0])
                radio.write("ACK")
                print("ACK sent")
                radio.openReadingPipe(1, pipe[1])
                radio.startListening()
                time.sleep(1)
                continue

            radio.read(received_data, radio.getDynamicPayloadSize())
            global received_data
            print(f"Received: {received_data}")
            time.sleep(1)


