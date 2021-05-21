# PC-To-Pi 소켓통신

1. pc_server_Thread.py에서 ip를 서버가 될 pc나 도커ip로 수정 후 실행.
2. pi_client_Thread.py에서 ip를 서버ip로 바꾸고 라즈베리 파이에서 실행
3. pc_server_Thread.py가 실행되는 경로에 test.wav 파일이 생성되면 프로그램이 자동 실행됨(스레드 처리로 5초에 한번씩 탐지 - 전송 or 파일없음 출력)
4. pi_client_Thread.py는 5초에 한번 자동실행되게 스레드 처리. 서버가 파일 안보내면 waiting 출력. 서버가 보내오면 /home/pi경로에 다운로드 - 음원 실행 - 삭제 실행