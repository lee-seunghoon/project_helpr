import RPi.GPIO as GPIO # 라즈베리파이 GPIO 핀을 쓰기위해 임포트
import time # 시간 간격으로 제어하기 위해 임포트
import paho.mqtt.client as mqtt

LED = 21
GPIO.setmode(GPIO.BCM)  # 핀의 번호를 보드 기준으로 설정, BCM은 GPIO 번호로 호출함
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW) #LED setup

#블라인드 DC모터용
in1 = 24
in2 = 18
en = 25
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(25)


#탁상 DC모터용
in3 = 13
in4 = 19
enb = 26
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p2 = GPIO.PWM(enb, 1000)
p2.start(25)


class MyMqtt_Sub():
    def __init__(self):

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        self.state = 85
        self.led_out = GPIO.output(LED, GPIO.LOW)
        self.led_on = GPIO.output(LED,GPIO.HIGH)
        self.pwm2 = GPIO.PWM(LED, 500)
        self.blindstate = 50


        client.connect("192.168.0.212", 1883, 60)
        client.loop_forever()



    def on_connect(self, client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("mycafe/servo")
            client.subscribe("mycafe/ledCustom")
            client.subscribe("mycafe/blind")
        # elif rc ==1:
        #     client.subscribe("mycafe/ledCustom")
        else:
            print("연결실패")



    def on_message(self, client, userdata, msg):
        myval = msg.payload.decode("utf-8")
        print(msg.topic + "----" + str(myval))

        if myval[0] == 't':
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            p2.ChangeDutyCycle(50)
            time.sleep(1)
            p2.ChangeDutyCycle(0)
            print("up")
        elif myval[0] == 'k':
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            p2.ChangeDutyCycle(50)
            time.sleep(1)
            p2.ChangeDutyCycle(0)
            print("down")

        elif myval[0] == 'l':
            if myval == 'light_up' and self.state < 100:
                self.state = self.state + 5
                self.pwm2.ChangeDutyCycle(self.state)

            elif self.state >= 100:
                self.state = 100
                self.led_on

            elif myval == 'light_down' and self.state > 0:
                self.state = self.state - 5
                self.pwm2.ChangeDutyCycle(self.state)

            elif self.state <= 0:
                self.state = 0
                self.led_out
            print(self.state)

        elif myval[0] == 'c':
            if self.blindstate < 100:
                self.blindstate = self.blindstate + 5
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                p.ChangeDutyCycle(50)
                time.sleep(1)
                p.ChangeDutyCycle(0)
                print("up")

        elif myval[0] == 'd':
            if self.blindstate > 0:
                self.blindstate = self.blindstate - 5
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                p.ChangeDutyCycle(50)
                time.sleep(1)
                p.ChangeDutyCycle(0)
                print("down")

        else:
            pass


if __name__ == "__main__":
    try:
        mymqtt = MyMqtt_Sub()

    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
        p.stop()
        p2.stop()