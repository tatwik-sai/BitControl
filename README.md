# BitControl - PC Controller via Micro:bit

## 1. Introduction

This document details the "BitControl" project, which enables users to wirelessly control various PC operations and play games using a micro:bit as a controller. The communication between the micro:bit and the PC is established via Bluetooth Low Energy (BLE). This project offers a menu-based interface on the micro:bit, allowing users to select different control modes for interacting with their computer.

[Watch Demo Video](https://youtu.be/riiqlc9271I)

---

## 2. Team Members

| S.No | Name                | Roll Number |
| ---- | ------------------- | ----------- |
| 1    | Molleti Tatwik Sai  |  BT2024200           |
| 2    | Madire Shiva Reddy  |  BT2024218           |
| 3    | Mohammed Farhan     |  BT2024140           |
| 4    | Saketh Boyina       | BT2024085            |
| 5    | Rohith Sai Manne    | BT2024144            |
| 6    | Sunnapu Suhith Reddy |  BT2024066           |
| 7    | Repalle Dhanush     |  BT2024155           |

---

## 3. Prerequisites

Before running the project, ensure you have the following installed on your PC:

* **Python 3.6 or higher:** This project is developed using Python.
* **pip (Python Package Installer):** Used to install the necessary Python libraries.
* **Bluetooth Adapter:** Your PC needs a functioning Bluetooth adapter.
* **Required Python Libraries:** Install the following libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```
    * **bleak:** For Bluetooth Low Energy communication with the micro:bit.
    * **keyboard:** To simulate keyboard presses on the PC.
    * **comtypes:** A COM interoperability package (required by pycaw on Windows).
    * **screen-brightness-control:** To control the PC's screen brightness.
    * **pycaw:** To control the PC's audio volume on Windows.
    * **pygame:** For rendering the graphical user interface (GUI) for the Pong and Car Dodge games.

> **Note:** This project works primarily for the windows operating system. The code may need modifications to work on other operating systems.
---

## 4. Installation and Running the Project

Follow these steps to install and run BitControl:

1.  **Flash Code to Micro:bit:**
    * Copy the the `mictobit-proj.hex` file onto your micro:bit using a suitable data transfer cable.

2.  **Enable Bluetooth on PC:**
    * Ensure that Bluetooth is turned on your PC.

3.  **Run the Server Script:**
    * Open a terminal or command prompt on your PC.
    * Navigate to the directory containing the project files (including `server.py`).
    * Run the server script using the following command:

        ```bash
        python server.py
        ```

    * Upon successful initiation of the Bluetooth connection with the micro:bit, a **(√) Tick Mark** will be displayed on the micro:bit. If the connection is lost at any point, a **(X) Cross Mark** will be displayed on the micro:bit.

---

## 5. Available Control Options, Navigation, Selection, and Controls

The micro:bit provides a menu-based interface to select different PC control options.

### 5.1. Navigation

* **Button A:** Moves the selection cursor to the **Left** within the menu.
* **Button B:** Moves the selection cursor to the **Right** within the menu.

### 5.2. Selection

* **Button A + Button B (pressed simultaneously):** Pressing both Button A and Button B at the same time **selects** the currently highlighted option in the menu.

### 5.3. Exiting an Option

* **Flip Micro:bit:** To exit most control options and return to the main menu, **flip the micro:bit over** (detecting a change in accelerometer orientation).

### 5.4. Control Options and Their Controls

The following control options are available:

1.  **Pong Game:**
    ```
        █ . . . .
        █ . . . .
        █ . . . █
        . . █ . █
        . . . . █
    ```

    * **Activation:** Select "Pong Game" from the menu and press Button A + Button B.
    * **GUI:** Touching the "Touch Sensor" on the micro:bit will start the Pong game on the PC or pauses it.
    * **Controls:**
        * **Touch Logo:** Touching it **Plays** or **Pauses** the game.
        * **Button A(Hold):** Move the player's paddle to the **Left** (along the X-axis).
        * **Button B(Hold):** Move the player's paddle to the **Right** (along the X-axis).
    * **Exit:** Flip the micro:bit.

2.  **Car Dodge Game:**

    ```
        . . █ . .
        . █ █ █ .
        . █ █ █ .
        █ █ █ █ █
        . █ . █ .
    ```

    * **Activation:** Select "Car Dodge" from the menu and press Button A + Button B.
    * **GUI:** This will open a GUI window on the PC for the Car Dodge game.
    * **Controls:**
        * **Touch Logo:** Touching it **Plays** or **Pauses** the game.
        * **Tilt Left:** Steer the player's car to the **Left**.
        * **Tilt Right:** Steer the player's car to the **Right**.
    * **Exit:** Flip the micro:bit.

3.  **Spotify Control:**
    ```
        . . . . .
        . █ █ █ .
        . █ . █ .
        █ █ . █ █
        █ █ . █ █
    ```
    * **Activation:** Select this option from the menu and press Button A + Button B.
    * **Controls:**
        * **Touch Logo:** Touching it **Plays** or **Pauses** the game.
        * **Tilt Left:** Decrease the Volume by 5%.
        * **Tilt Right:** Increase the Volume by 5%.
        * **Button A:** Move to the previous track.
        * **Button B:** Move to the next track.
    * **Exit:** Flip the micro:bit.

4.  **Brightness Control:**
    ```
        . . █ . .
        . █ . █ .
        █ . █ . █
        . █ . █ .
        . . █ . .
    ```
    * **Activation:** Select "Brightness" from the menu and press Button A + Button B.
    * **Controls:**
        * **Button A:** Decrease the PC's screen brightness.
        * **Button B:** Increase the PC's screen brightness.
    * **Exit:** Flip the micro:bit.

5.  **Lock PC (One-Step Action):** 

     ```
        . █ █ █ .
        . █ . █ .
        █ █ █ █ █
        █ . . . █
        █ █ █ █ █
     ```

    * **Activation:** Select "Lock PC" from the menu and press Button A + Button B.
    * **Action:** This will immediately lock your PC. There is no separate exit for this action.

6.  **Shutdown PC (One-Step Action):**

    ```
        █ █ █ █ █
        █ . . . █
        █ . █ . █
        █ . . . █
        █ █ █ █ █
    ```

    * **Activation:** Select "Shutdown" from the menu and press Button A + Button B.
    * **Action:** This will immediately initiate the shutdown process of your PC. There is no separate exit for this action.

---

## 6. Server-Side Code(`server.py`)

The `server.py` script running on the PC is responsible for:

* **Bluetooth LE Connection:** Scanning for and establishing a connection with the micro:bit. It uses the `bleak` library for this purpose.
* **Data Reception:** Receiving data sent from the micro:bit over the established BLE connection.
* **PC Control Logic:** Interpreting the received data and performing the corresponding actions on the PC using libraries like `keyboard`, `pycaw`, and `screen_brightness_control`.
* **Game Logic:** Implementing the backend logic for the Pong and Car Dodge games using `pygame`, including game state management, object movement, collision detection, and scoring.
* **UART Emulation (Internal):** Simulates UART communication over the BLE connection to send data to and receive data from the micro:bit.
* **Menu Handling (Internal):** Manages the menu options and their corresponding codes.
* **Accelerometer Data Streaming (for "Car" control):** Continuously polls accelerometer data from the micro:bit when the "Car Dodge" option is active.
* **Button Press Handling:** Detects and processes button presses (single and simultaneous) from the micro:bit.
* **Touch Sensor Input:** Detects input from the micro:bit's touch sensor and notifies.
* **Shake and Logo Up/Down Detection:** Interprets specific micro:bit gestures (shake, logo up/down).
* **Game Rendering (GUI):** Uses `pygame` to create and update the graphical interface for the Pong and Car Dodge games.

The server script likely contains a main loop that continuously:

1.  Scans for the micro:bit if not connected.
2.  Establishes and maintains the BLE connection.
3.  Receives data from the micro:bit.
4.  Parses the received data to determine the user's intended action (menu navigation, option selection, game controls).
5.  Executes the corresponding PC control function or updates the game state

> **Note:** The bluetooth connection and UART data transfer is implemented from scratch with out using any prebuild librarys in the server side. The code is written in Python and uses the `bleak`, `btooth` library for Bluetooth communication.
---

## 7. Micro:bit Code(`mictobit_python.py`)

The Python code flashed onto the micro:bit is responsible for:

* **Bluetooth LE Advertising:** Making the micro:bit discoverable by the PC server.
* **Connection Handling:** Establishing and maintaining the BLE connection with the PC server.
* **Menu Display:** Displaying the menu options (Pong Game, Car Dodge, Volume, Brightness, Lock PC, Shutdown) on the micro:bit's LED matrix.
* **Button Input:** Reading input from Button A and Button B presses (single and simultaneous).
* **Accelerometer Reading:** Reading the micro:bit's accelerometer data to detect flips and stream data for the "Car Dodge" control.
* **Touch Sensor Reading:** Detecting touch input on the micro:bit's capacitive touch sensor.
* **Gesture Detection:** Detecting specific gestures like shake and logo up/down.
* **UART Emulation (Internal):** Simulating UART communication over the BLE connection to send control commands and sensor data to the PC server.
* **Data Transmission:** Sending the detected button presses, accelerometer data, touch sensor input, and gestures to the PC server over the BLE connection.
* **Connection Status Indication:** Displaying a tick mark (√) on the LED matrix when the Bluetooth connection is active and a cross mark (X) when the connection is lost.
* **Menu Navigation Logic:** Implementing the logic for moving the selection cursor left and right based on button presses.
* **Option Selection Logic:** Detecting simultaneous presses of Button A and Button B to select the current menu option.
* **Exit Logic:** Detecting a flip of the micro:bit to trigger the exit from a control option.

The micro:bit code contains a main loop that continuously:

1.  Initializes Bluetooth and advertises its presence.
2.  Handles connection requests from the PC server.
3.  Monitors button presses, accelerometer readings, and touch sensor input.
4.  Updates the menu display based on user input.
5.  Sends the relevant control data to the connected PC server via BLE.
6.  Updates the connection status indicator on the LED matrix.
---
