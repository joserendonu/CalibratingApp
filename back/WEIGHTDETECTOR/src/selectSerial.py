import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def get_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def create_serial_combobox(parent, x, y, variable, exclude_port=None):
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if exclude_port and exclude_port in ports:
        ports.remove(exclude_port)

    combo = ttk.Combobox(parent, textvariable=variable, values=ports, state="readonly", width=12)
    combo.place(x=x, y=y)
    return combo