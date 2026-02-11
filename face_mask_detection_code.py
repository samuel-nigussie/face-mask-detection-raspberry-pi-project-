#!/usr/bin/python
import spidev
import time
import os
import RPi.GPIO as GPIO
import pio
import Ports

pio.uart = Ports.UART()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

spi = spidev.SpiDev()
spi.open(0, 0)

LCD_RS, LCD_E = 7, 11
LCD_D4, LCD_D5, LCD_D6, LCD_D7 = 12, 13, 15, 16
Motor_1, Motor_2 = 29, 31
temp_channel = 0

E_PULSE, E_DELAY, delay = 0.0005, 0.0005, 1
LCD_WIDTH, LCD_CHR, LCD_CMD = 16, True, False
LCD_LINE_1, LCD_LINE_2 = 0x80, 0xC0

for pin in [LCD_E, LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7, Motor_1, Motor_2]:
    GPIO.setup(pin, GPIO.OUT)

def lcd_init():
    for cmd in [0x33, 0x32, 0x06, 0x0C, 0x28, 0x01]:
        lcd_byte(cmd, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    for i, pin in enumerate([LCD_D4, LCD_D5, LCD_D6, LCD_D7]):
        GPIO.output(pin, bool(bits & (0x10 << i)))
    lcd_toggle_enable()
    for i, pin in enumerate([LCD_D4, LCD_D5, LCD_D6, LCD_D7]):
        GPIO.output(pin, bool(bits & (0x01 << i)))
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    lcd_byte(line, LCD_CMD)
    for char in message.ljust(LCD_WIDTH)[:LCD_WIDTH]:
        lcd_byte(ord(char), LCD_CHR)

def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def ConvertTemp(data, places):
    return round((data * 330) / 1023.0, places)

lcd_init()
lcd_string("welcome ", LCD_LINE_1)
time.sleep(1)
lcd_byte(0x01, LCD_CMD)
lcd_string("Waiting for data...", LCD_LINE_1)

while True:
    if pio.uart.recv() == "1":
        lcd_byte(0x01, LCD_CMD)
        lcd_string(" Mask Detected", LCD_LINE_1)
        time.sleep(2)
        temp = ConvertTemp(ReadChannel(temp_channel), 2)
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Temperature  ", LCD_LINE_1)
        lcd_string(str(temp), LCD_LINE_2)
        time.sleep(2)
        
        if 90 < temp < 100:
            lcd_byte(0x01, LCD_CMD)
            lcd_string("Gate Open", LCD_LINE_2)
            GPIO.output(Motor_1, True)
            GPIO.output(Motor_2, False)
            time.sleep(1)
            GPIO.output(Motor_1, False)
            GPIO.output(Motor_2, True)
            time.sleep(1)
        else:
            lcd_byte(0x01, LCD_CMD)
            lcd_string("High Temperature  ", LCD_LINE_1)
            lcd_string("Gate close", LCD_LINE_2)
        GPIO.output(Motor_1, False)
        GPIO.output(Motor_2, False)
        time.sleep(1)
    else:
        lcd_byte(0x01, LCD_CMD)
        lcd_string(" Mask not ", LCD_LINE_1)
        lcd_string(" Detected ", LCD_LINE_2)
        time.sleep(0.5)
