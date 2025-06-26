import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def get_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def create_serial_combobox(root, x=0, y=0, variable=None, state="readonly"):
    ports = [port.device for port in serial.tools.list_ports.comports()]
    
    combo = ttk.Combobox(
        root,
        values=ports,
        textvariable=variable,
        state=state,           # ← obligatorio para que sea solo seleccionable
        font=("Arial", 12),
        width=10
    )
    combo.place(x=x, y=y)

    if ports and variable:
        variable.set(ports[0])  # ← selecciona automáticamente el primero
    
    return combo


