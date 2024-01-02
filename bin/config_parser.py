import configparser
import os

def parse_config(file_path='.\config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)

    # Получение значения из секции и ключа
    config.get('SectionName', '')

    os.environ.update({
        'MAIN_CAMERA': config.get('SectionName', 'MAIN_CAMERA'),
        'EXAMPLE_INTEGER_VALUE': str(example_integer_value),
        'EXAMPLE_BOOLEAN_VALUE': str(example_boolean_value),
        'EXAMPLE_FLOAT_VALUE': str(example_float_value),
        'EXAMPLE_LIST_VALUE': ','.join(example_list_value),
        'EXAMPLE_VALUE_WITH_DEFAULT': example_value_with_default,
    })
