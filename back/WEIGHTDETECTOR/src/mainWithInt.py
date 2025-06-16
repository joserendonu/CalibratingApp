import tkinter as tk
from tkinter import messagebox
import serial
import threading

# --- Comunicación Serial ---
ser = serial.Serial('COM4', 9600, timeout=1)
serial_data = []

def read_serial():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                serial_data.append(line)
                if len(serial_data) > 100:
                    serial_data.pop(0)
                update_output_text("\n".join(serial_data[-5:]))
                update_display_fields(line)
        except Exception as e:
            print("Error:", e)

def send_serial(command):
    try:
        ser.write((command + "\n").encode('utf-8'))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Funciones de botones ---
def set_zero():
    send_serial("set_zero")

def set_scale():
    scale = entry_escala_izq.get()
    send_serial(f"set_scale:{scale}")

def enviar_comando():
    comando = entry_comando_extra.get()
    send_serial(comando)

# --- Actualización campos UI ---
def update_output_text(text):
    txt_salida.delete("1.0", tk.END)
    txt_salida.insert(tk.END, text)

def update_display_fields(line):
    if "peso:" in line and "escala:" in line:
        parts = dict(part.split(":") for part in line.split(","))
        entry_peso.delete(0, tk.END)
        entry_peso.insert(0, parts.get("peso", "0.000"))
        entry_escala_der.delete(0, tk.END)
        entry_escala_der.insert(0, parts.get("escala", "0.00"))

# --- Ventana principal ---
root = tk.Tk()
root.title("Calibración")
root.geometry("850x500")
root.configure(bg="lightblue")

# --- Etiquetas y campos ---
tk.Label(root, text="Calibración", font=("Arial", 20, "bold"), bg="lightblue").place(x=320, y=10)

# Escala izquierda
tk.Label(root, text="Escala", font=("Arial", 14), bg="lightblue").place(x=220, y=60)
entry_escala_izq = tk.Entry(root, font=("Arial", 12), width=6, justify="right")
entry_escala_izq.place(x=220, y=90)

tk.Button(root, text="Set escala", command=set_scale, font=("Arial", 12), width=12).place(x=100, y=90)
tk.Button(root, text="Set cero", command=set_zero, font=("Arial", 12), width=12).place(x=100, y=50)

# Peso patrón y botón Enviar Comando
tk.Label(root, text="Peso Patrón", font=("Arial", 14), bg="lightblue").place(x=10, y=180)
entry_peso_patron = tk.Entry(root, font=("Arial", 12), width=5, justify="right")
entry_peso_patron.insert(0, f"{5.0:.3f}")
entry_peso_patron.place(x=140, y=175)
tk.Label(root, text="Kg", font=("Arial", 14), bg="lightblue").place(x=210, y=180)

tk.Button(root, text="Enviar Comando", command=enviar_comando, font=("Arial", 12), width=14).place(x=100, y=220)

# Campo adicional al lado del botón "Enviar Comando"
entry_comando_extra = tk.Entry(root, font=("Arial", 12), width=7, justify="right")
entry_comando_extra.place(x=250, y=220)

# Parte derecha (peso y escala)
tk.Label(root, text="Peso", font=("Arial", 14), bg="lightblue").place(x=500, y=60)
entry_peso = tk.Entry(root, font=("Arial", 12), width=7, justify="right")
entry_peso.place(x=560, y=55)
tk.Label(root, text="Kg", font=("Arial", 14), bg="lightblue").place(x=680, y=60)

tk.Label(root, text="Escala", font=("Arial", 14), bg="lightblue").place(x=500, y=100)
entry_escala_der = tk.Entry(root, font=("Arial", 12), width=6, justify="right")
entry_escala_der.place(x=580, y=95)

# Área de salida
tk.Label(root, text="Salida (en Kg)", font=("Arial", 14), bg="lightblue").place(x=400, y=150)
txt_salida = tk.Text(root, font=("Arial", 12), width=40, height=6)
txt_salida.place(x=400, y=180)

# Hilo de lectura serial
threading.Thread(target=read_serial, daemon=True).start()

root.mainloop()
