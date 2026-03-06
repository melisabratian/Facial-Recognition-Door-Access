import serial

# Serial Communication Functions
def open_serial_connection(port, baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.is_open:
            print(f"Connected to {port} at {baudrate} baud.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")

def close_serial_connection(ser):
    if ser.is_open:
        ser.close()
        print("Connection closed.")

def send_data(ser, data):
    if ser.is_open:
        print(f"Sending: {data}")
        ser.write(data.encode())  # Send data as bytes
    else:
        print("Serial port not open!")

def receive_data(ser):
    if ser.is_open:
        while True:  # Keep waiting until data is received
            data = ser.readline()  # Read a line of data (until newline)
            if data:  # Check if data is not empty
                decoded_data = data.decode('utf-8').strip()
                print(f"Received: {decoded_data}")
                return decoded_data
            # else:
            #     print("Waiting for data...")
    else:
        print("Serial port not open!")
        return None
