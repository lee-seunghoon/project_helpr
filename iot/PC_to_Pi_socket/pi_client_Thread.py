#라즈베리 파이(client)

#현재는 서버 코드
#클라 - 서버 코드 바꿔야함
#클라인데 라즈베리파이에서 파일 받기

import socket
import tqdm
import os
import threading
import time
# Server's IP address 192.168.0.9
HOST = "13.209.193.138" #116.120.114.71
PORT = 8000
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


def pi_client_Method():
    s = socket.socket()
    s.connect((HOST,PORT))

    try:
        received = s.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the client socket
        #client_socket.close()
        # close the server socket
        s.close()
        os.system("aplay /home/pi/test.wav")
        os.system("sudo rm /home/pi/test.wav")
    except:
        print("waiting")
        pass

    threading.Timer(5, pi_client_Method).start()

print("loading client_Thread....")
time.sleep(10)
pi_client_Method()