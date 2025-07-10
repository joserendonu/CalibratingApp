# main.py
import tkinter as tk
import threading
import serial
from fake_reader import read_encrypted_fake
#  --- nuevas importaciones ---
import reporter                               # ← importa el módulo recién creado
from tkinter import messagebox                # ← para avisar al usuario
from selectSerial import create_serial_combobox
from tkinter import ttk

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

# FUNCIONES
def abrir_puerto_pesos():
    global ser
    try:
        if ser and ser.is_open:
            ser.close()

        # --- Traducir valores de los Combobox a constantes de pyserial ---
        bytesize = {
            "5": serial.FIVEBITS,
            "6": serial.SIXBITS,
            "7": serial.SEVENBITS,
            "8": serial.EIGHTBITS
        }[selected_data_bits.get()]

        parity = {
            "None": serial.PARITY_NONE,
            "Even": serial.PARITY_EVEN,
            "Odd": serial.PARITY_ODD,
            "Mark": serial.PARITY_MARK,
            "Space": serial.PARITY_SPACE
        }[selected_parity.get()]

        stopbits = {
            "1": serial.STOPBITS_ONE,
            "1.5": serial.STOPBITS_ONE_POINT_FIVE,
            "2": serial.STOPBITS_TWO
        }[selected_stop_bits.get()]

        # Control de flujo
        flow = selected_flow_control.get()
        xonxoff = flow == "XON/XOFF"
        rtscts = flow == "RTS/CTS"
        dsrdtr = flow == "DSR/DTR"

        ser = serial.Serial(
            port=selected_port_pesos.get(),
            baudrate=int(selected_baudrate.get()),
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=1,
            xonxoff=xonxoff,
            rtscts=rtscts,
            dsrdtr=dsrdtr
        )
        print(f"[Serial abierto] {selected_port_pesos.get()} con {selected_baudrate.get()} baudios")
    except serial.SerialException as e:
        ser = None
        print(f"[Error] No se pudo abrir {selected_port_pesos.get()}: {e}")


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
    while True:
        try:
            if ser and ser.is_open:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    update_pesos(line)
            else:
                threading.Event().wait(0.1)  # espera corta para no bloquear CPU
        except Exception as e:
            print("[serial_reader error]:", e)  
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
    scale = entry_escala_izq.get().strip()
    
    if not scale:
        messagebox.showwarning("Advertencia", "Por favor escribe un valor de escala.")
        return
    send_serial(f"set_scale:{scale}")
    entry_escala_der.config(state='normal')
    entry_escala_der.delete(0, tk.END)
    entry_escala_der.insert(0, scale)
    entry_escala_der.config(state='readonly')
def enviar_comando():
    comando = entry_comando_extra.get().strip().lower()
    send_serial(comando)
    # Sincroniza botones si el comando es config o auto
    if comando == "config":
        btn_config.config(state="disabled")
        btn_auto.config(state="normal")
    elif comando == "auto":
        btn_auto.config(state="disabled")
        btn_config.config(state="normal")

# ========== UI ==========
root = tk.Tk()
root.title("CALIBRACIÓN")
root.geometry("900x500")
root.configure(bg="#aed6f1")

# --- Notebook (Tabs) ---
notebook = ttk.Notebook(root)
notebook.place(x=0, y=0, relwidth=1, height=620)  # Ajusta height si quieres más espacio para la tab
# Tab principal (puedes ponerle más widgets si quieres)
tab_main = tk.Frame(notebook, bg="#aed6f1")
notebook.add(tab_main, text="Calibración")
# Tab de configuración de puerto serial
tab_serial = tk.Frame(notebook, bg="#aed6f1")
notebook.add(tab_serial, text="Puerto Serial")

# Calcular tamaño dinámico
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.6)
window_height = int(screen_height * 0.7)
root.geometry(f"{window_width}x{window_height}")

root.configure(bg="#aed6f1")
selected_port_pesos = tk.StringVar(value=PORT)
selected_port_codigos = tk.StringVar(value=PORT)

# ===== CONFIGURACIÓN DE PARÁMETROS DE PUERTO SERIAL =====



# --- Valores posibles ---
baudrates = ["300", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"]
data_bits_options = ["5", "6", "7", "8"]
parity_options = ["None", "Even", "Odd", "Mark", "Space"]
stop_bits_options = ["1", "1.5", "2"]
flow_control_options = ["None", "XON/XOFF", "RTS/CTS", "DSR/DTR"]

# --- Variables seleccionadas ---
selected_baudrate = tk.StringVar(value="9600")
selected_data_bits = tk.StringVar(value="8")
selected_parity = tk.StringVar(value="None")
selected_stop_bits = tk.StringVar(value="1")
selected_flow_control = tk.StringVar(value="None")


# 🚀 Colocamos los comboboxes arriba
x_base = 30
y_base = 20
espacio_vertical = 30

ttk.Label(tab_serial, text="Baudrate:", background="#aed6f1").place(x=x_base, y=y_base)
ttk.Combobox(tab_serial, textvariable=selected_baudrate, values=baudrates, width=10, state="readonly").place(x=120, y=y_base)

ttk.Label(tab_serial, text="Data Bits:", background="#aed6f1").place(x=x_base, y=y_base + espacio_vertical)
ttk.Combobox(tab_serial, textvariable=selected_data_bits, values=data_bits_options, width=10, state="readonly").place(x=120, y=y_base + espacio_vertical)

ttk.Label(tab_serial, text="Parity:", background="#aed6f1").place(x=x_base, y=y_base + 2 * espacio_vertical)
ttk.Combobox(tab_serial, textvariable=selected_parity, values=parity_options, width=10, state="readonly").place(x=120, y=y_base + 2 * espacio_vertical)

ttk.Label(tab_serial, text="Stop Bits:", background="#aed6f1").place(x=x_base, y=y_base + 3 * espacio_vertical)
ttk.Combobox(tab_serial, textvariable=selected_stop_bits, values=stop_bits_options, width=10, state="readonly").place(x=120, y=y_base + 3 * espacio_vertical)

ttk.Label(tab_serial, text="Flow Control:", background="#aed6f1").place(x=x_base, y=y_base + 4 * espacio_vertical)
ttk.Combobox(tab_serial, textvariable=selected_flow_control, values=flow_control_options, width=10, state="readonly").place(x=120, y=y_base + 4 * espacio_vertical)

# 👇 Para que se reabra el puerto automáticamente
for var in [selected_baudrate, selected_data_bits, selected_parity, selected_stop_bits, selected_flow_control]:
    var.trace_add("write", lambda *args: abrir_puerto_pesos())

# ComboBox arriba de "Pesos recibidos"
create_serial_combobox(tab_main, x=400, y=30, variable=selected_port_pesos)
selected_port_pesos.trace_add("write", lambda *args: abrir_puerto_pesos())
abrir_puerto_pesos()  # Abrir puerto inicial antes del hilo
threading.Thread(target=read_serial, daemon=True).start()
# Recargar puerto al cambiar cualquier parámetro
# Recargar puerto al cambiar cualquier parámetro
for var in [selected_baudrate, selected_data_bits, selected_parity, selected_stop_bits, selected_flow_control]:
    var.trace_add("write", lambda *args: abrir_puerto_pesos())
# PESO PATRÓN
tk.Label(tab_main, text="Peso Patrón", font=("Arial", 14), bg="#aed6f1").place(x=30, y=100)
entry_peso_patron = tk.Entry(tab_main, font=("Arial", 12), width=6, justify="right")
entry_peso_patron.insert(0, "5.000")
entry_peso_patron.place(x=140, y=102)
tk.Label(tab_main, text="Kg", font=("Arial", 14), bg="#aed6f1").place(x=200, y=102)



# PESO y ESCALA (derecha)
tk.Label(tab_main, text="Peso", font=("Arial", 14), bg="#aed6f1").place(x=30, y=140)
entry_peso = tk.Entry(tab_main, font=("Arial", 12), width=6, justify="right", state='readonly')
entry_peso.place(x=100, y=140)
tk.Label(tab_main, text="Kg", font=("Arial", 14), bg="#aed6f1").place(x=170, y=140)

entry_escala_der = tk.Entry(tab_main, font=("Arial", 12), width=6, justify="right", state='readonly', readonlybackground="white", fg="black")
entry_escala_der.insert(0, "1")  # ← aquí sí se inicializa en 1
entry_escala_der.place(x=100, y=40)
tk.Label(tab_main, text="Escala", font=("Arial", 14), bg="#aed6f1").place(x=30, y=180)
entry_escala_der.place(x=100, y=180)
colorAuto = "#27ae60"
colorConfig = "#c0392b"

def enviar_config():
    entry_comando_extra.delete(0, tk.END)
    entry_comando_extra.insert(0, "config")
    enviar_comando()
    btn_config.config(state="disabled")
    btn_auto.config(state="normal")
    entry_escala_izq.config(state="normal")  # ← Deshabilita input de escala
def enviar_auto():
    entry_comando_extra.delete(0, tk.END)
    entry_comando_extra.insert(0, "auto")
    enviar_comando()
    btn_auto.config(state="disabled")
    btn_config.config(state="normal")
    entry_escala_izq.config(state="disabled")    # ← Habilita input de escala
btn_config = tk.Button(
    tab_main,
    text="Config",
    command=enviar_config,
    font=("Arial", 12),
    bg=colorConfig,
    fg="white",
    activebackground=colorConfig,
    state="normal"
)
# BOTONES
btn_config.place(x=30, y=320)

btn_auto = tk.Button(
    tab_main,
    text="Auto",
    command=enviar_auto,
    font=("Arial", 12),
    bg=colorAuto,
    fg="white",
    activebackground=colorAuto,
    state="disabled"  # Deshabilitado al inicio
)
btn_auto.place(x=130, y=320)
tk.Label(tab_main, text="Pesos recibidos",
         font=("Arial", 14), bg="#aed6f1").place(x=500, y=30)
txt_salida = tk.Text(tab_main, font=("Arial", 12), 
                     width=30, height=6)  # width reducido
txt_salida.place(x=400, y=60)  # x igual, pero puedes reducir si quieres más margen

# CÓDIGOS ENCRIPTADOS
tk.Label(tab_main, text="Códigos encriptados", font=("Arial", 14), bg="#aed6f1").place(x=500, y=220)
txt_codigos = tk.Text(tab_main, font=("Arial", 12), width=30, height=6)  # igual que txt_salida
txt_codigos.place(x=400, y=250)  # igual que txt_salida

# BOTONES
tk.Button(tab_main, text="Set cero", command=set_zero, font=("Arial", 12)).place(x=50, y=400)
tk.Button(tab_main, text="Set escala", command=set_scale, font=("Arial", 12)).place(x=50, y=440)
#  --- botón en la interfaz (coordenadas aproximadas) ---
tk.Button(tab_main,
          text="Generar reporte",
          command=generar_reporte_ui,
          font=("Arial", 12)
          ).place(x=320, y=445)                # ajusta X/Y si lo prefieres

entry_escala_izq = tk.Entry(tab_main, font=("Arial", 12), width=6, justify="right")
entry_escala_izq.place(x=160, y=445)
tk.Label(tab_main, text="Escala", font=("Arial", 12), bg="#aed6f1").place(x=230, y=445)

# COMANDO EXTRA
tk.Button(tab_main, text="Enviar Comando", command=enviar_comando, font=("Arial", 12)).place(x=500, y=440)
entry_comando_extra = tk.Entry(tab_main, font=("Arial", 12), width=8, justify="right")
entry_comando_extra.place(x=640, y=443)

entry_escala_izq.delete(0, tk.END)
entry_escala_izq.insert(0, "1")
set_scale()
entry_escala_izq.config(state="disabled")
# HILOS
# threading.Thread(target=read_serial, daemon=True).start()
threading.Thread(target=lambda: read_encrypted_fake(update_codigos), daemon=True).start()



root.mainloop()
