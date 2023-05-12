#!/bin/bash
# Script to test 16x2 LCD matrix display on Raspberry Pi 3B+

# Set up the GPIO pins for the LCD display
sudo gpio -g mode 18 out
sudo gpio -g mode 23 out
sudo gpio -g mode 24 out
sudo gpio -g mode 25 out

# Initialize the LCD display
sudo sh -c "echo 0 > /sys/class/gpio/gpio25/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio24/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio23/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio18/value"
sudo sh -c "echo 1 > /sys/class/gpio/gpio18/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio24/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio23/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio25/value"
sudo sh -c "echo 0 > /sys/class/gpio/gpio18/value"

# Send commands to display text on the LCD
echo -e '\x1b[2J' > /dev/tty1
echo -e '\x1b[0;0f' > /dev/tty1
echo "Testing 16x2 LCD display" > /dev/tty1
echo -e '\x1b[1;0f' > /dev/tty1
echo "Hello World!" > /dev/tty1

# Clean up the GPIO pins
sudo gpio -g mode 18 in
sudo gpio -g mode 23 in
sudo gpio -g mode 24 in
sudo gpio -g mode 25 in
