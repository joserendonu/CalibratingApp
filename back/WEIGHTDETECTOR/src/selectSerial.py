import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def get_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def create_serial_combobox(root, x, y, variable, width=15):
    combo = ttk.Combobox(root, values=get_serial_ports(), textvariable=variable, state="readonly", width=width)
    combo.place(x=x, y=y)
    return combo