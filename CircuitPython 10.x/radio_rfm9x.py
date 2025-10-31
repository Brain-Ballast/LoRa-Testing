# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x



# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0, 115200)
rfm9x.tx_power = 23
prev_packet = None
packet_count = 0

while True:
    packet = None

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        print("Waiting for PKT...")
    else:
        prev_packet = packet
        packet_count += 1
        try:
            packet_text = str(prev_packet, "utf-8")
            print(f"Received #{packet_count}: {packet_text}")
        except UnicodeDecodeError:
            print(f"Received #{packet_count}: [Raw bytes] {prev_packet}")
        
        # Don't sleep after receiving - immediately check for more packets
        continue
    
    # Only sleep when no packet received to avoid blocking reception
    time.sleep(0.01)  # Much shorter sleep for better responsiveness
