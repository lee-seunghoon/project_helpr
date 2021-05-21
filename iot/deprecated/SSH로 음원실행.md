# ~~SSH 실행~~ (같은 대역폭에서만 사용가능)

1.  ai_answer_play는 ai_answer 폴더에 음성파일이 생성되는걸 감지

2. 생성을 감지(외부에서 SSH로 음원을 전송해 오면)하면 4초간 대기(업로드 대기)후 실행

3. 실행 후 삭제



* SSH scp 전송할때 라즈베리파이 암호 요구 안하게 하는 법

  -> https://robotai.tistory.com/18

  

scp <Docker or PC 경로>testaudio.wav pi@192.168.0.181:/home/pi/iot/mic/ai_answer

* 자동화 예정(아마 EC2 도커 쪽에서 AI 음성 합성 프로그램이 돌고 음원을 만들어내면 그걸 전송하기)



#### ai_answer_play.py

* 라즈베리 파이의 /home/pi/iot/mic/ai_answer 폴더를 감시하다 파일이 들어오면 실행 후 삭제하는 프로그램
* Pi 부팅 후 자동실행되게 설정완료

