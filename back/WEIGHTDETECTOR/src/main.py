
# import serial
# import threading
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import uvicorn

# app = FastAPI()
# serial_data = []

# def read_serial():
#     with serial.Serial('COM4', 9600, timeout=1) as ser:
#         while True:
#             line = ser.readline().decode('utf-8').strip()
#             if line:
#                 print(f"Recibido: {line}")
#                 serial_data.append(line)
#                 # Limita el tamaño de la lista
#                 if len(serial_data) > 100:
#                     serial_data.pop(0)

# @app.get("/serial")
# def get_serial_data():
#     # Devuelve los últimos datos recibidos
#     return {"data": serial_data[-10:]}

# @app.post("/serial")
# async def send_serial_data(request: Request):
#     body = await request.json()
#     data = body.get("data", "")
#     with serial.Serial('COM4', 9600, timeout=1) as ser:
#         ser.write((data + '\n').encode('utf-8'))
#     return JSONResponse(content={"status": "sent", "data": data})

# if __name__ == "__main__":
#     threading.Thread(target=read_serial, daemon=True).start()
#     uvicorn.run(app, host="0.0.0.0", port=8000)
import serial
import threading
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
serial_data = []
ser = serial.Serial('COM4', 9600, timeout=1)  # Abrir solo una vez
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica tu origen
    allow_credentials=True,
    allow_methods=["*"],  # O ["POST", "OPTIONS"]
    allow_headers=["*"],
)
def read_serial():
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f"Recibido: {line}")
            serial_data.append(line)
            if len(serial_data) > 100:
                serial_data.pop(0)

@app.get("/serial")
def get_serial_data():
    return {"data": serial_data[-10:]}

@app.post("/serial")
async def send_serial_data(request: Request):
    body = await request.json()
    data = body.get("data", "")
    ser.write((data + '\n').encode('utf-8'))  # Usar el mismo objeto serial
    return JSONResponse(content={"status": "sent", "data": data})

if __name__ == "__main__":
    threading.Thread(target=read_serial, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
