# fake_reader.py
import random
import string
import time

def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def read_encrypted_fake(callback, delay=1.0):
    """
    Genera un código encriptado falso cada *delay* segundos
    y lo envía al callback que se le pase como argumento.
    """
    while True:
        code = generar_codigo()
        callback(code)
        time.sleep(delay)
