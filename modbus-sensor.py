from pymodbus.client.sync import ModbusSerialClient
import time
import os

class XYMD01Sensor:
    def __init__(self, port='COM3', slave_id=1):
        self.port = port
        self.slave_id = slave_id
        self.client = ModbusSerialClient(
            method='rtu',
            port=port,
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )
        
        # Modbus register addresses
        self.REGISTERS = {
            'temperature': 0x0001,    # Input register
            'humidity': 0x0002,       # Input register
            'device_address': 0x0101, # Keep register
            'baud_rate': 0x0102,      # Keep register
            'temp_correction': 0x0103, # Keep register
            'hum_correction': 0x0104   # Keep register
        }
        
        # Baud rate options
        self.BAUD_RATES = {
            0: 9600,
            1: 14400,
            2: 19200
        }

    def connect(self):
        """Connect to the sensor"""
        return self.client.connect()
        
    def disconnect(self):
        """Disconnect from the sensor"""
        self.client.close()
        
    def read_measurements(self):
        """Read temperature and humidity values"""
        try:
            # Read both temperature and humidity at once
            response = self.client.read_input_registers(
                address=self.REGISTERS['temperature'],
                count=2,
                unit=self.slave_id
            )
            
            if not response.isError():
                temperature = response.registers[0] / 10.0
                humidity = response.registers[1] / 10.0
                return temperature, humidity
            else:
                print("Error reading values")
                return None, None
                
        except Exception as e:
            print(f"Error communicating with sensor: {str(e)}")
            return None, None



    def change_modbus_address(self, new_address):
        """Change the Modbus device address"""
        try:
            if 1 <= new_address <= 247:
                # در اینجا از دستور 0x06 برای تغییر آدرس استفاده می‌کنیم
                response = self.client.write_register(
                    address=0x0101,      # آدرس رجیستر Device Address
                    value=new_address,   # آدرس جدید
                    unit=self.slave_id,
                    function_code=0x06   # از فانکشن کد 0x06 استفاده می‌کنیم
                )
                
                if not response.isError():
                    print(f"Successfully changed Modbus address to: {new_address}")
                    print("Please power cycle the sensor for the new address to take effect")
                    self.slave_id = new_address
                    return True
                else:
                    print("Error changing Modbus address")
                    print("Response:", response)
                    return False
            else:
                print("Invalid Modbus address. Please use a value between 1 and 247.")
                return False
        except Exception as e:
            print(f"Error changing Modbus address: {str(e)}")
            return False


    def change_baud_rate(self, baud_index):
        """Change the sensor's baud rate"""
        try:
            if baud_index in self.BAUD_RATES:
                response = self.client.write_register(
                    address=self.REGISTERS['baud_rate'],
                    value=baud_index,
                    unit=self.slave_id
                )
                if not response.isError():
                    print(f"Successfully changed baud rate to: {self.BAUD_RATES[baud_index]}")
                    return True
                else:
                    print("Error changing baud rate")
                    return False
            else:
                print("Invalid baud rate index. Use 0 (9600), 1 (14400), or 2 (19200)")
                return False
        except Exception as e:
            print(f"Error changing baud rate: {str(e)}")
            return False

    def set_temperature_correction(self, correction):
        """Set temperature correction value"""
        try:
            if -100 <= correction <= 100:
                # Multiply by 10 to convert to sensor format
                correction_value = int(correction * 10)
                response = self.client.write_register(
                    address=self.REGISTERS['temp_correction'],
                    value=correction_value,
                    unit=self.slave_id
                )
                if not response.isError():
                    print(f"Successfully set temperature correction to: {correction}")
                    return True
                else:
                    print("Error setting temperature correction")
                    return False
            else:
                print("Invalid correction value. Use value between -10.0 and 10.0")
                return False
        except Exception as e:
            print(f"Error setting temperature correction: {str(e)}")
            return False

    def set_humidity_correction(self, correction):
        """Set humidity correction value"""
        try:
            if -100 <= correction <= 100:
                # Multiply by 10 to convert to sensor format
                correction_value = int(correction * 10)
                response = self.client.write_register(
                    address=self.REGISTERS['hum_correction'],
                    value=correction_value,
                    unit=self.slave_id
                )
                if not response.isError():
                    print(f"Successfully set humidity correction to: {correction}")
                    return True
                else:
                    print("Error setting humidity correction")
                    return False
            else:
                print("Invalid correction value. Use value between -10.0 and 10.0")
                return False
        except Exception as e:
            print(f"Error setting humidity correction: {str(e)}")
            return False

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_input(prompt, min_val, max_val):
    """Get validated numeric input from user"""
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a value between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number")

def main_menu():
    """Main program menu"""
    clear_screen()
    print("=== XY-MD01 Temperature & Humidity Sensor ===")
    address = int(get_valid_input("Enter sensor Modbus address (1-247): ", 1, 247))
    
    sensor = XYMD01Sensor(port='COM3', slave_id=address)
    
    if not sensor.connect():
        print("Error connecting to sensor")
        return
        
    while True:
        clear_screen()
        print("\n=== Main Menu ===")
        print("1. Read Temperature and Humidity")
        print("2. Change Modbus Address")
        print("3. Change Baud Rate")
        print("4. Set Temperature Correction")
        print("5. Set Humidity Correction")
        print("6. Exit")
        
        choice = int(get_valid_input("Enter your choice (1-6): ", 1, 6))
        
        if choice == 1:
            clear_screen()
            print("\n=== Reading Sensor Data ===")
            temp, hum = sensor.read_measurements()
            if temp is not None and hum is not None:
                print(f"Temperature: {temp}°C")
                print(f"Humidity: {hum}%")
            input("\nPress Enter to continue...")
            
        elif choice == 2:
            clear_screen()
            print("\n=== Change Modbus Address ===")
            new_address = int(get_valid_input("Enter new Modbus address (1-247): ", 1, 247))
            if sensor.change_modbus_address(new_address):
                sensor.disconnect()
                print("Please restart the program and connect with the new address")
                return
            input("\nPress Enter to continue...")
            
        elif choice == 3:
            clear_screen()
            print("\n=== Change Baud Rate ===")
            print("Available baud rates:")
            print("0: 9600")
            print("1: 14400")
            print("2: 19200")
            baud_index = int(get_valid_input("Enter baud rate index (0-2): ", 0, 2))
            if sensor.change_baud_rate(baud_index):
                sensor.disconnect()
                print("Please restart the program with the new baud rate")
                return
            input("\nPress Enter to continue...")
            
        elif choice == 4:
            clear_screen()
            print("\n=== Set Temperature Correction ===")
            correction = get_valid_input("Enter temperature correction (-10.0 to 10.0): ", -10.0, 10.0)
            sensor.set_temperature_correction(correction)
            input("\nPress Enter to continue...")
            
        elif choice == 5:
            clear_screen()
            print("\n=== Set Humidity Correction ===")
            correction = get_valid_input("Enter humidity correction (-10.0 to 10.0): ", -10.0, 10.0)
            sensor.set_humidity_correction(correction)
            input("\nPress Enter to continue...")
            
        elif choice == 6:
            sensor.disconnect()
            print("Goodbye!")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")