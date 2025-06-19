import tkinter as tk
from tkinter import messagebox
import serial, threading, random, string, time

# ---------- CONFIGURACIÓN ----------
PORT      = "COM4"
BAUDRATE  = 9600
# -----------------------------------

# Abrir el puerto CH340
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
except serial.SerialException as e:
    ser = None
    print(f"¡Aviso! No se pudo abrir {PORT}: {e}")

serial_data     = []     # Historial de pesos
encrypted_data  = []     # Historial de códigos encriptados

# ---------- FUNCIONES DE COM ----------
def read_serial():
    """Lee pesos reales desde COM4 (si está disponible)."""
    if not ser:
        return
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                procesar_peso(line)
        except Exception as e:
            print("Error COM4:", e)

def procesar_peso(line):
    serial_data.append(line)
    if len(serial_data) > 100:
        serial_data.pop(0)
    update_output_text("\n".join(serial_data[-5:]))
    update_display_fields(line)

# ---------- CÓDIGOS ENCRIPTADOS (FAKE) ----------
def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def read_encrypted_fake():
    """Genera un código aleatorio cada segundo y lo muestra."""
    while True:
        code = generar_codigo()
        encrypted_data.append(code)
        if len(encrypted_data) > 100:
            encrypted_data.pop(0)
        update_encrypted_text("\n".join(encrypted_data[-10:]))
        time.sleep(1)

# ---------- ENVÍO DE COMANDOS ----------
def send_serial(command):
    if ser:
        try:
            ser.write((command + "\n").encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        print(f"(COM4 no abierto) > {command}")

def set_zero():
    send_serial("set_zero")

def set_scale():
    scale = entry_escala_izq.get()
    send_serial(f"set_scale:{scale}")

def enviar_comando():
    comando = entry_comando_extra.get()
    send_serial(comando)

# ---------- ACTUALIZAR UI ----------
def update_output_text(text):
    txt_salida.delete("1.0", tk.END)
    txt_salida.insert(tk.END, text)

def update_encrypted_text(text):
    txt_codigos.delete("1.0", tk.END)
    txt_codigos.insert(tk.END, text)

def update_display_fields(line):
    if "peso:" in line and "escala:" in line:
        try:
            parts = dict(part.split(":") for part in line.split(","))
            entry_peso.delete(0, tk.END)
            entry_peso.insert(0, parts.get("peso", "0.000"))
            entry_escala_der.delete(0, tk.END)
            entry_escala_der.insert(0, parts.get("escala", "0.00"))
        except ValueError:
            pass  # línea con formato inesperado

# ---------- INTERFAZ ----------
root = tk.Tk()
root.title("Calibración")
root.geometry("850x600")
root.configure(bg="lightblue")

tk.Label(root, text="Calibración", font=("Arial", 20, "bold"),
         bg="lightblue").place(x=320, y=10)

# Escala izquierda
tk.Label(root, text="Escala", font=("Arial", 14),
         bg="lightblue").place(x=220, y=60)
entry_escala_izq = tk.Entry(root, font=("Arial", 12), width=6, justify="right")
entry_escala_izq.place(x=220, y=90)

tk.Button(root, text="Set escala", command=set_scale,
          font=("Arial", 12), width=12).place(x=100, y=90)
tk.Button(root, text="Set cero", command=set_zero,
          font=("Arial", 12), width=12).place(x=100, y=50)

# Peso patrón
tk.Label(root, text="Peso Patrón", font=("Arial", 14),
         bg="lightblue").place(x=10, y=180)
entry_peso_patron = tk.Entry(root, font=("Arial", 12),
                             width=5, justify="right")
entry_peso_patron.insert(0, f"{5.0:.3f}")
entry_peso_patron.place(x=140, y=175)
tk.Label(root, text="Kg", font=("Arial", 14),
         bg="lightblue").place(x=210, y=180)

tk.Button(root, text="Enviar Comando", command=enviar_comando,
          font=("Arial", 12), width=14).place(x=100, y=220)

entry_comando_extra = tk.Entry(root, font=("Arial", 12),
                               width=7, justify="right")
entry_comando_extra.place(x=250, y=220)

# Peso y escala a la derecha
tk.Label(root, text="Peso", font=("Arial", 14),
         bg="lightblue").place(x=500, y=60)
entry_peso = tk.Entry(root, font=("Arial", 12),
                      width=7, justify="right")
entry_peso.place(x=560, y=55)
tk.Label(root, text="Kg", font=("Arial", 14),
         bg="lightblue").place(x=680, y=60)

tk.Label(root, text="Escala", font=("Arial", 14),
         bg="lightblue").place(x=500, y=100)
entry_escala_der = tk.Entry(root, font=("Arial", 12),
                            width=6, justify="right")
entry_escala_der.place(x=580, y=95)

# Área de salida: pesos
tk.Label(root, text="Pesos recibidos", font=("Arial", 14),
         bg="lightblue").place(x=400, y=150)
txt_salida = tk.Text(root, font=("Arial", 12),
                     width=40, height=6)
txt_salida.place(x=400, y=180)

# Área de códigos encriptados
tk.Label(root, text="Códigos encriptados", font=("Arial", 14),
         bg="lightblue").place(x=400, y=320)
txt_codigos = tk.Text(root, font=("Arial", 12),
                      width=40, height=6)
txt_codigos.place(x=400, y=350)

# ---------- HILOS ----------
threading.Thread(target=read_serial, daemon=True).start()
threading.Thread(target=read_encrypted_fake, daemon=True).start()

root.mainloop()
