#!/usr/local/bin/python
import RPi.GPIO as GPIO
from gpiozero import LED
import time
import paho.mqtt.client as mqtt


#MQTT
Broker_URL = "50c69f01d2b349de8f734066b3b5a261.s1.eu.hivemq.cloud"
Broker_Port = "8883"
Topic_IR = "IR"
Topic_LDR = "LDR"
client = mqtt.Client()
client.username_pw_set("User1", "User1234")
client.tls_set()
client.connect(broker_url, broker_port)
#Hardware Pins
led_pins = [17, 18, 27, 22, 23, 24]
ir_sensors = [4, 17, 27,6]
ldr_pin = 4  

#Initializing IR Sensors 
for sensor in ir_sensors:
    GPIO.setup(sensor, GPIO.IN)

#Initializing LEDs 
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
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

#Function Actions based on LDR Value
def is_night():
  LDR_Value = rc_time(ldr_pin)
  client.publish(Topic_LDR,LDR_Value,qos=1)
  if ldr_value > 2500:
    return False
  else:
    return True

#Function to Control LEDs 
def control_leds(sensor_index):
    if is_night():
        if 0 <= sensor_index < len(led_pins) // 2:
            GPIO.output(led_pins[sensor_index * 2], GPIO.HIGH)
            GPIO.output(led_pins[sensor_index * 2 + 1], GPIO.HIGH)
    else:
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)

#Operating IR with LDR 
try:
    while True:
        for i, pin in enumerate(ir_sensors):
			IR_Value = GPIO.input(pin)
			client.publish(Topic_IR,IR_Value,qos=1)
            if IR_Value == GPIO.LOW:
                control_leds(i)
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
