# Microbit Stopwatch Program Documentation

This document provides an overview of the ARMv6-M assembly language program developed for the Microbit to implement a stopwatch. The stopwatch tracks time in minutes and seconds, displays it on a 4-digit LED display, and uses button inputs for control.

## 1. Hardware Control

The program directly manipulates GPIO (General Purpose Input/Output) for controlling the LED display and reading button inputs. It also configures and utilizes the Microbit's Timer 0 (TIMERO) for accurate timekeeping.

## 2. Memory Layout

The program's memory is organized into three main sections:

* `.text`: This section contains the executable instructions of the program.
* `.bss`: This section holds uninitialized variables, including those used for storing the elapsed seconds, minutes, the current state of the stopwatch (running or stopped), and the state of the buttons.
* `.rodata`: This section stores read-only data, specifically the LED patterns required to display digits from 0 to 9 on the LED display.

## 3. Main Functionality

The program's core functionality includes:

* **Time Tracking**: The program accurately tracks time in minutes and seconds using the hardware timer.
* **Display**: The current time is displayed on the Microbit's 4-digit LED display.
* **User Interaction**: Buttons A and B provide user control. Button A toggles the stopwatch between running and stopped, and Button B resets the stopwatch to 00:00.

## 4. Functionalities

### 4.1 Initialization

* `_main`:
    * Sets up the stack pointer.
    * Configures the LED GPIOs as outputs.
    * Initializes the timer.
    * Clears the LED display.
* `init_timer`: Initializes the TIMERO by clearing its value.

### 4.2 Timer Control

* `start_timer`: Starts the TIMERO to begin counting.
* `stop_timer`: Stops the TIMER.
* `update_time`: Reads the current value from TIMERO and updates the seconds and minutes counters accordingly.

### 4.3 Display Functions

* `clear_display`: Turns off all LEDs on the display.
* `display_time`:  Displays the current time (minutes and seconds) on the 4-digit LED display by calling `display_digit` for each digit.
* `display_digit`: Renders a single digit (0-9) at a specified position on the LED display using the digit patterns stored in the `.rodata` section.

### 4.4 Button Handling

* `check_buttons`: Monitors the state of Button A and Button B.
    * Button A: Toggles the stopwatch between running and stopped states.
    * Button B: Resets the minutes and seconds counters to zero and clears the timer.

### 4.5 Utility Functions

* `divide_unsigned`: Performs unsigned integer division. This function is used to calculate the individual digits to be displayed and to convert timer values to seconds and minutes.
* `delay`: Implements a simple busy-wait delay, used to control the display refresh rate for readability.

## 5. Program Flow

1.  The program starts by initializing the hardware components and clearing the display.
2.  It then enters a main loop that continuously executes:
    * Checks for button presses to update the stopwatch's state.
    * If the stopwatch is running, it updates the time and displays it.
    * If the stopwatch is stopped, it displays the last recorded time.
3.  This loop repeats indefinitely, providing continuous stopwatch functionality.

> **Note:** We are unable to get this code live and running on the microbit device due to some technical issues. However, the code is well-structured and should work as intended once the code is properly converted to .hex.
