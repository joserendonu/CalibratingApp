import serial
import threading

def read_codigos_serial(update_codigos_callback, port, baudrate, bytesize, parity, stopbits, xonxoff, rtscts, dsrdtr):
    try:
        ser_codigos = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=1,
            xonxoff=xonxoff,
            rtscts=rtscts,
            dsrdtr=dsrdtr
        )
    except Exception as e:
        print(f"[codigo_reader] No se pudo abrir {port}: {e}")
        return

    def loop():
        while True:
            try:
                if ser_codigos and ser_codigos.is_open:
                    line = ser_codigos.readline().decode('utf-8').strip()
                    if line:
                        update_codigos_callback(line)
            except Exception as e:
                print("[codigo_reader error]:", e)
                break

    threading.Thread(target=loop, daemon=True).start()