from microbit import *

def on_bluetooth_connected():
    global choosen, option, num_options, text_list
    choosen = 0
    option = 0
    num_options = 5
    text_list = ["Pong", "Music", "Lock", "Car", "Brightness", "Shutdown"]
    basic.show_icon(IconNames.YES)
    basic.pause(200)
    Showicon()
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def Showicon():
    if option == 0:
        basic.show_leds("""
            # . . . .
            # . . . .
            # . . . #
            . . # . #
            . . . . #
            """)
    elif option == 1:
        basic.show_leds("""
            . . . . .
            . # # # .
            . # . # .
            # # . # #
            # # . # #
            """)
    elif option == 2:
        basic.show_leds("""
            . # # # .
            . # . # .
            # # # # #
            # . . . #
            # # # # #
            """)
    elif option == 3:
        basic.show_leds("""
            . . # . .
            . # # # .
            . # # # .
            # # # # #
            . # . # .
            """)
    elif option == 4:
        basic.show_leds("""
            . . # . .
            . # . # .
            # . # . #
            . # . # .
            . . # . .
            """)
    else:
        basic.show_leds("""
            # # # # #
            # . . . #
            # . # . #
            # . . . #
            # # # # #
            """)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.NO)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_button_pressed_a():
    global option
    if choosen == 0:
        if option > 0:
            option = option - 1
        else:
            option = num_options
        Showicon()
    else:
        bluetooth.uart_write_string("A")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_gesture_logo_up():
    bluetooth.uart_write_string("LU")
input.on_gesture(Gesture.LOGO_UP, on_gesture_logo_up)

def on_gesture_tilt_left():
    bluetooth.uart_write_string("TL")
input.on_gesture(Gesture.TILT_LEFT, on_gesture_tilt_left)

def on_gesture_screen_down():
    global choosen
    if choosen == 1:
        choosen = 0
        bluetooth.uart_write_string("Stop")
input.on_gesture(Gesture.SCREEN_DOWN, on_gesture_screen_down)

def on_uart_data_received():
    basic.show_string(bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE)))
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

def on_button_pressed_ab():
    global choosen
    if choosen == 0:
        if option != 2 and option != 5:
            choosen = 1
        bluetooth.uart_write_string(text_list[option])
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global option
    if choosen == 0:
        if option < num_options:
            option = option + 1
        else:
            option = 0
        Showicon()
    else:
        bluetooth.uart_write_string("B")
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_gesture_shake():
    bluetooth.uart_write_string("S")
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def on_gesture_tilt_right():
    bluetooth.uart_write_string("TR")
input.on_gesture(Gesture.TILT_RIGHT, on_gesture_tilt_right)

def on_gesture_logo_down():
    bluetooth.uart_write_string("LD")
input.on_gesture(Gesture.LOGO_DOWN, on_gesture_logo_down)

def on_logo_pressed():
    bluetooth.uart_write_string("LP")
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

text_list: List[str] = []
num_options = 0
option = 0
choosen = 0
bluetooth.start_uart_service()

def on_every_interval():
    if choosen == 1:
        if option == 3:
            bluetooth.uart_write_string(convert_to_text(input.acceleration(Dimension.X)))
        else:
            if input.button_is_pressed(Button.A):
                bluetooth.uart_write_string("AP")
            if input.button_is_pressed(Button.B):
                bluetooth.uart_write_string("BP")
loops.every_interval(100, on_every_interval)
