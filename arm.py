import socket

# ESP32 IP address and port (replace with your ESP32 IP)
esp32_ip = '192.168.166.80'
esp32_port = 8080

# Connect to ESP32
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((esp32_ip, esp32_port))

try:
    while True:
        command = input("Enter command (or 'q' to quit): ")  # Take user input
        if command.lower() == 'q':  # Exit loop if user enters 'q'
            break
        client.send(command.encode())  # Send command to ESP32

except KeyboardInterrupt:
    print("\nConnection closed.")

finally:
    client.close()  # Close the connection

#a = backward
#b = forward
#c  = left
#d = right