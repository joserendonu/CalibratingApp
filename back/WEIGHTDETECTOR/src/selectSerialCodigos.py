# archivo: selectSerialCodigos.py

import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports



def create_codigos_serial_selector(parent, x=0, y=0, variable_port=None, on_change_callback=None):
    ports = [port.device for port in serial.tools.list_ports.comports()]
    combo = ttk.Combobox(parent, textvariable=variable_port, values=ports, state="readonly", width=12)
    combo.place(x=x, y=y)

    """
    Crea un conjunto de widgets para seleccionar puerto y parámetros del puerto de códigos reales.
    """
    # Variables para los parámetros
    baudrates = ["300", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"]
    data_bits_options = ["5", "6", "7", "8"]
    parity_options = ["None", "Even", "Odd", "Mark", "Space"]
    stop_bits_options = ["1", "1.5", "2"]
    flow_control_options = ["None", "XON/XOFF", "RTS/CTS", "DSR/DTR"]

    # Variables Tkinter
    selected_baudrate = tk.StringVar(value="9600")
    selected_data_bits = tk.StringVar(value="8")
    selected_parity = tk.StringVar(value="None")
    selected_stop_bits = tk.StringVar(value="1")
    selected_flow_control = tk.StringVar(value="None")

    # Widgets
    ttk.Label(parent, text="Puerto códigos:").place(x=x, y=y)
    port_combobox = ttk.Combobox(parent, textvariable=variable_port, values=get_serial_ports(), width=10, state="readonly")
    port_combobox.place(x=x + 120, y=y)

    ttk.Label(parent, text="Baudrate:").place(x=x, y=y + 30)
    ttk.Combobox(parent, textvariable=selected_baudrate, values=baudrates, width=10, state="readonly").place(x=x + 120, y=y + 30)

    ttk.Label(parent, text="Data Bits:").place(x=x, y=y + 60)
    ttk.Combobox(parent, textvariable=selected_data_bits, values=data_bits_options, width=10, state="readonly").place(x=x + 120, y=y + 60)

    ttk.Label(parent, text="Parity:").place(x=x, y=y + 90)
    ttk.Combobox(parent, textvariable=selected_parity, values=parity_options, width=10, state="readonly").place(x=x + 120, y=y + 90)

    ttk.Label(parent, text="Stop Bits:").place(x=x, y=y + 120)
    ttk.Combobox(parent, textvariable=selected_stop_bits, values=stop_bits_options, width=10, state="readonly").place(x=x + 120, y=y + 120)

    ttk.Label(parent, text="Flow Control:").place(x=x, y=y + 150)
    ttk.Combobox(parent, textvariable=selected_flow_control, values=flow_control_options, width=10, state="readonly").place(x=x + 120, y=y + 150)

    # Actualizar puerto si se cambia algo
    def update_config(*args):
        if on_change_callback:
            config = {
                "baudrate": int(selected_baudrate.get()),
                "bytesize": {
                    "5": serial.FIVEBITS,
                    "6": serial.SIXBITS,
                    "7": serial.SEVENBITS,
                    "8": serial.EIGHTBITS
                }[selected_data_bits.get()],
                "parity": {
                    "None": serial.PARITY_NONE,
                    "Even": serial.PARITY_EVEN,
                    "Odd": serial.PARITY_ODD,
                    "Mark": serial.PARITY_MARK,
                    "Space": serial.PARITY_SPACE
                }[selected_parity.get()],
                "stopbits": {
                    "1": serial.STOPBITS_ONE,
                    "1.5": serial.STOPBITS_ONE_POINT_FIVE,
                    "2": serial.STOPBITS_TWO
                }[selected_stop_bits.get()],
                "xonxoff": selected_flow_control.get() == "XON/XOFF",
                "rtscts": selected_flow_control.get() == "RTS/CTS",
                "dsrdtr": selected_flow_control.get() == "DSR/DTR",
            }
            on_change_callback(config)

    for var in [selected_baudrate, selected_data_bits, selected_parity, selected_stop_bits, selected_flow_control]:
        var.trace_add("write", update_config)
    
    return combo


# Utilidad para obtener puertos disponibles
import serial.tools.list_ports

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]
