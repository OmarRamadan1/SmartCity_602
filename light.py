#!/usr/local/bin/python
import RPi.GPIO as GPIO
from gpiozero import LED
import time
#import paho.mqtt.client as mqtt

#MQTT
#Broker_URL = "50c69f01d2b349de8f734066b3b5a261.s1.eu.hivemq.cloud"
#Broker_Port = "8883"
#Topic_IR = "IR"
#Topic_LDR = "LDR"
#client = mqtt.Client()
#client.username_pw_set("User1", "User1234")
#client.tls_set()
#client.connect(broker_url, broker_port)

#Hardware Pins
GPIO.setmode(GPIO.BOARD)
#led_pins = [35, 37, 36, 38]
LED_Pin_1 = LED(19)
LED_Pin_2 = LED(26)
LED_Pin_3 = LED(16)
LED_Pin_4 = LED(20)
#ir_sensors = [11, 13, 15,18]
IR_Sensor_1 = 11
IR_Sensor_2 = 13
IR_Sensor_3 = 15
IR_Sensor_4 = 16
pin_to_circuit = 12 

#Initializing IR Sensors 
#for sensor in ir_sensors:
#    GPIO.setup(sensor, GPIO.IN)
GPIO.setup(IR_Sensor_1,GPIO.IN)
GPIO.setup(IR_Sensor_2,GPIO.IN)
GPIO.setup(IR_Sensor_3,GPIO.IN)
GPIO.setup(IR_Sensor_4,GPIO.IN)


    
#Getting LDR Value
def rc_time (pin_to_circuit):
    count = 0
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pin_to_circuit, GPIO.IN)

    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count
try:
    while True:
            IR_Value_1 = GPIO.input(IR_Sensor_1)
            IR_Value_2 = GPIO.input(IR_Sensor_2)
            IR_Value_3 = GPIO.input(IR_Sensor_3)
            IR_Value_4 = GPIO.input(IR_Sensor_4)
            LDR_Value = rc_time(pin_to_circuit)
            #print(LDR_Value)
#  client.publish(Topic_LDR,LDR_Value,qos=1)
            if LDR_Value > 2500:
                if not IR_Value_1:
                    LED_Pin_1.on()
                    LED_Pin_2.off()
                    LED_Pin_3.off()
                    LED_Pin_4.off()
                elif not IR_Value_2:
                    LED_Pin_1.off()
                    LED_Pin_2.on()
                    LED_Pin_3.off()
                    LED_Pin_4.off()
                elif not IR_Value_3:
                    LED_Pin_1.off()
                    LED_Pin_2.off()
                    LED_Pin_3.on()
                    LED_Pin_4.off()
                elif not IR_Value_4:
                    LED_Pin_1.off()
                    LED_Pin_2.off()
                    LED_Pin_3.off()
                    LED_Pin_4.on()	
				#return False
            else:
                LED_Pin_1.off()
                LED_Pin_2.off()
                LED_Pin_3.off()
                LED_Pin_4.off()
                #print("Light")

                
            time.sleep(0.05)                
#			client.publish(Topic_IR,IR_Value,qos=1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()