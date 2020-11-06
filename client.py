import io
import socket
import struct
import time
import picamera
import sys
import ConfigParser

if __name__ == "__main__":
    config_path = "./config.conf"

    config = ConfigParser.ConfigParser()
    config.read(config_path)

    SERVER_ADDRESS = config['settings']['SERVER_ADDRESS']
    SERVER_PORT = config['settings']['SERVER_PORT']

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            print("starting Camera...........")
            time.sleep(2)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
    finally:
        connection.close()
        client_socket.close()
