enum Mode
{
    CONFIG,
    AUTO
};

Mode mode = AUTO;               // Default mode is AUTO
unsigned long lastSendTime = 0; // Para controlar el tiempo con millis
int timeSeconds = 2000;         // Tiempo en milisegundos para enviar datos
long scale = 103;

void setup()
{
    Serial.begin(9600);
    randomSeed(analogRead(0)); // Initialize random seed
}
void loop()
{
    if (Serial.available() > 0)
    {
        String data = Serial.readStringUntil('\n'); // Read data until newline
        if (data == "config")
        {
            mode = CONFIG; // Switch to CONFIG mode
            Serial.println("Switched to CONFIG mode. You can now set scale, calibrate, or set zero.");
        }
        else if (data == "auto")
        {
            mode = AUTO; // Switch to AUTO mode
            Serial.println("Switched to AUTO mode. Data will be sent every 2 seconds.");
        }
        else if (mode == CONFIG)
        {
            if (data == "calibrate")
            {
                Serial.println("Calibrating..."); // Placeholder for calibration logic
                // Aquí puedes agregar la lógica de calibración si es necesario
            }
            else if (data == "setZero")
            {
                Serial.println("Setting zero..."); // Placeholder for setting zero logic
                // Aquí puedes agregar la lógica para establecer el cero si es necesario
            }
            else if (data == "getScale")
            {
                Serial.print("Current scale: ");
                Serial.println(scale); // Print the current scale value
            }
            else if (data.startsWith("setScale "))
            {
                String scaleStr = data.substring(9); // Get the scale value after "setScale "
                scale = scaleStr.toInt();            // Convert to integer
                Serial.print("Scale set to: ");
                Serial.println(scale);
            }
            else if (data == "getMode")
            {
                Serial.print("Current mode: ");
                Serial.println(mode == CONFIG ? "CONFIG" : "AUTO");
            }
            else
            {
                Serial.println("Unknown command. Please use 'config', 'auto', 'calibrate', 'setZero', 'getScale', 'setScale <value>', or 'getMode'.");
            }
        }
        else
        {
            Serial.println("Unknown command. Please switch to CONFIG mode to set parameters.");
        }
    }
    // Solo enviar datos cada 2 segundos usando millis y si está en modo CONFIG
    if (mode == AUTO && millis() - lastSendTime >= timeSeconds)
    {
        Serial.println(random(1000)); // Print a random number between 0 and 999
        lastSendTime = millis();
    } // Wait for 1 second
}
