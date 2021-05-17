# SSH 실행

6. ai_answer_play는 ai_answer 폴더에 음성파일이 생성되는걸 감지
2. 생성을 감지(외부에서 SSH로 음원을 전송해 오면)하면 4초간 대기(업로드 대기)후 실행
3. 실행 후 삭제



scp <Docker or PC 경로>testaudio.wav pi@192.168.0.XX:/home/pi/iot/mic/ai_answer

* 자동화 예정