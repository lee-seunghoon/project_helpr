import paho.mqtt.client as mqtt

LED = 21


class Led_Mqtt():
    def __init__(self,state,led_out,led_on,pwm):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message


        client.connect("192.168.0.180", 1883, 60)
        client.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("stt/test")
        else:
            print("connect fail..")

    def on_message(self, client, userdata, msg):
        myval = msg.payload.decode("utf-8")
        print(myval)


if __name__ == "__main__":
    try:
        mymqtt = Led_Mqtt(0,None,None,None)

    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()

