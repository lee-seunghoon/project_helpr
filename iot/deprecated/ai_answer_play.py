import os
import time
while True:
    temp = os.path.isfile('/home/pi/iot/mic/ai_answer/testaudio.wav')
    if temp == True:
        print(temp)
        time.sleep(3)
        #os.system("aplay --format=S16_LE --rate=16000 /home/pi/iot/mic/ai_answer/testaudio.wav")
        os.system("aplay /home/pi/iot/mic/ai_answer/testaudio.wav")
        os.system("sudo rm /home/pi/iot/mic/ai_answer/testaudio.wav")
#
        
# import os
# import time
# 
# time.sleep(4)
# #os.system("aplay --format=S16_LE --rate=16000 /home/pi/iot/mic/ai_answer/testaudio.wav")
# os.system("sudo aplay /home/pi/iot/mic/ai_answer/testaudio.wav")
# os.system("sudo rm /home/pi/iot/mic/ai_answer/testaudio.wav")
