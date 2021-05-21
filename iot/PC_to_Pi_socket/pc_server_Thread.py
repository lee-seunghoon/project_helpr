#파일 보내는거 (서버 -> 파이)
#서버 파일임!!!!!!!

import socket
import os
import tqdm
import time
from threading import Thread
import threading

# Server IP or Hostname
SERVER_HOST = "13.209.193.138"  
SERVER_PORT = 8000
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def pc_serverMethod():
    filename = 'testaudio.wav'
    #filesize = os.path.getsize(filename)

    # Pick an open Port (1000+ recommended), must match the client sport
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))  # 연결해줄 서버와 포트 결합

    s.listen(5)  # 클라 연결 대기
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    client_socket, address = s.accept()  # 서버 소켓 s에 클라이언트 소켓, 주소 연결 요청 수락
    print(f"[+] {address} is connected.")  # 클라이언트(Pi)연결되면 출력

    if os.path.isfile(filename) == True:
        print("file detected")
        filesize = os.path.getsize(filename)
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode()) #클라 소켓으로 send

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                client_socket.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        #client_socket.close()
        time.sleep(5)
        os.remove('C:/IoT/work/iotwork/iotserver/socket/firsttest/testaudio.wav') # wav 삭제 dir

    else:
        print("파일없음")
        pass

    threading.Timer(5, pc_serverMethod).start()

pc_serverMethod()