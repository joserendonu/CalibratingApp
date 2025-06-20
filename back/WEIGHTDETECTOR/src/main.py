# main.py
import tkinter as tk
import threading
import serial
from fake_reader import read_encrypted_fake
#  --- nuevas importaciones ---
import reporter                               # ← importa el módulo recién creado
from tkinter import messagebox                # ← para avisar al usuario

# ========== CONFIG ==========
PORT = "COM4"
BAUDRATE = 9600

# ========== COM SETUP ==========
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
except serial.SerialException as e:
    ser = None
    print(f"[serial_reader] Cannot open {PORT}: {e}")

# ========== DATA ==========
serial_data = []
encrypted_data = []
#  --- función a invocar desde el botón ---
def generar_reporte_ui():
    try:
        ruta = reporter.generar_reporte(serial_data.copy())   # ❷ copia para evitar conflictos con el hilo
        messagebox.showinfo("Reporte creado",
                            f"Se guardó en:\n{ruta}")
    except Exception as e:
        messagebox.showerror("Error al generar reporte", str(e))

# ========== SERIAL FUNCTIONS ==========
def read_serial():
    if not ser:
        return
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                update_pesos(line)
        except Exception as e:
            print("[serial_reader error]:", e)

def send_serial(command):
    if ser:
        try:
            ser.write((command + "\n").encode('utf-8'))
        except Exception as e:
            print("Serial error:", e)
    else:
        print(f"(COM4 cerrado) > {command}")

# ========== UI UPDATE ==========
def update_pesos(line):
    serial_data.append(line)
    if len(serial_data) > 100:
        serial_data.pop(0)
    txt_salida.delete("1.0", tk.END)
    txt_salida.insert(tk.END, "\n".join(serial_data[-5:]))
    entry_peso.config(state='normal')
    entry_peso.delete(0, tk.END)
    entry_peso.insert(0, line)
    entry_peso.config(state='readonly')


def update_codigos(codigo):
    encrypted_data.append(codigo)
    if len(encrypted_data) > 100:
        encrypted_data.pop(0)
    txt_codigos.delete("1.0", tk.END)
    txt_codigos.insert(tk.END, "\n".join(encrypted_data[-10:]))

# ========== COMMAND ACTIONS ==========
def set_zero():
    send_serial("set_zero")

def set_scale():
    scale = entry_escala_izq.get()
    send_serial(f"set_scale:{scale}")
    entry_escala_der.config(state='normal')
    entry_escala_der.delete(0, tk.END)
    entry_escala_der.insert(0, scale)
    entry_escala_der.config(state='readonly')

def enviar_comando():
    comando = entry_comando_extra.get()
    send_serial(comando)

# ========== UI ==========
root = tk.Tk()
root.title("CALIBRACIÓN")
root.geometry("900x500")
root.configure(bg="#aed6f1")

# PESO PATRÓN
tk.Label(root, text="Peso Patrón", font=("Arial", 14), bg="#aed6f1").place(x=20, y=40)
entry_peso_patron = tk.Entry(root, font=("Arial", 12), width=6, justify="right")
entry_peso_patron.insert(0, "5.000")
entry_peso_patron.place(x=140, y=42)
tk.Label(root, text="Kg", font=("Arial", 14), bg="#aed6f1").place(x=200, y=40)

# PESO y ESCALA (derecha)
tk.Label(root, text="Peso", font=("Arial", 14), bg="#aed6f1").place(x=20, y=100)
entry_peso = tk.Entry(root, font=("Arial", 12), width=6, justify="right", state='readonly')
entry_peso.place(x=100, y=100)
tk.Label(root, text="Kg", font=("Arial", 14), bg="#aed6f1").place(x=170, y=100)

tk.Label(root, text="Escala", font=("Arial", 14), bg="#aed6f1").place(x=20, y=140)
entry_escala_der = tk.Entry(root, font=("Arial", 12), width=6, justify="right", state='readonly')
entry_escala_der.insert(0, "0")
entry_escala_der.place(x=100, y=140)

# PESOS RECIBIDOS
tk.Label(root, text="Pesos recibidos", font=("Arial", 14), bg="#aed6f1").place(x=500, y=30)
txt_salida = tk.Text(root, font=("Arial", 12), width=38, height=6)
txt_salida.place(x=500, y=60)

# CÓDIGOS ENCRIPTADOS
tk.Label(root, text="Códigos encriptados", font=("Arial", 14), bg="#aed6f1").place(x=500, y=220)
txt_codigos = tk.Text(root, font=("Arial", 12), width=38, height=6)
txt_codigos.place(x=500, y=250)

# BOTONES
tk.Button(root, text="Set cero", command=set_zero, font=("Arial", 12)).place(x=50, y=400)
tk.Button(root, text="Set escala", command=set_scale, font=("Arial", 12)).place(x=50, y=440)
#  --- botón en la interfaz (coordenadas aproximadas) ---
tk.Button(root,
          text="Generar reporte",
          command=generar_reporte_ui,
          font=("Arial", 12)
          ).place(x=320, y=445)                # ajusta X/Y si lo prefieres

entry_escala_izq = tk.Entry(root, font=("Arial", 12), width=6, justify="right")
entry_escala_izq.place(x=160, y=445)
tk.Label(root, text="Escala", font=("Arial", 12), bg="#aed6f1").place(x=230, y=445)

# COMANDO EXTRA
tk.Button(root, text="Enviar Comando", command=enviar_comando, font=("Arial", 12)).place(x=600, y=440)
entry_comando_extra = tk.Entry(root, font=("Arial", 12), width=10, justify="right")
entry_comando_extra.place(x=740, y=443)

# HILOS
threading.Thread(target=read_serial, daemon=True).start()
threading.Thread(target=lambda: read_encrypted_fake(update_codigos), daemon=True).start()

root.mainloop()
