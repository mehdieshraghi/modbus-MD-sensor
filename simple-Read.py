from pymodbus.client.sync import ModbusSerialClient

# تنظیمات ارتباط سریال
client = ModbusSerialClient(
    method='rtu',
    port='COM3',  # شماره پورت سریال
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

# برقراری ارتباط
if client.connect():
    print("Connected to Modbus device")

    # خواندن دما (رجیستر 0x0001)
    temp = client.read_input_registers(address=0x0001, count=1, unit=1)
    if temp.isError():
        print("Error reading temperature")
    else:
        temperature = temp.registers[0] / 10  # تقسیم بر 10 برای مقدار صحیح
        print(f"Temperature: {temperature} °C")

    # خواندن رطوبت (رجیستر 0x0002)
    hum = client.read_input_registers(address=0x0002, count=1, unit=1)
    if hum.isError():
        print("Error reading humidity")
    else:
        humidity = hum.registers[0] / 10  # تقسیم بر 10 برای مقدار صحیح
        print(f"Humidity: {humidity} %")

    # قطع ارتباط
    client.close()
else:
    print("Failed to connect to Modbus device")
