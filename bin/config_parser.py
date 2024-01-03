import configparser
import os


def parse_config(file_path='.\\config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)

    os.environ.update({
        'MAIN_CAMERA': config.get('CAMERA', 'MAIN_CAMERA'),
        'CE_PIN': config.get('NRF_COMM', 'CE_PIN'),
        'CSN_PIN': config.get('NRF_COMM', 'CSN_PIN'),
        'NRF_CHANNEL': config.get('NRF_COMM', 'NRF_CHANNEL'),
        'PIPE_RX': config.get('NRF_COMM', 'PIPE_RX'),
        'PIPE_TX': config.get('NRF_COMM', 'PIPE_TX'),
        'PAYLOAD_SIZE': config.get('NRF_COMM', 'PAYLOAD_SIZE'),
        'DRONE_IP': config.get('DRONE_CONTROL', 'DRONE_IP')
    })
