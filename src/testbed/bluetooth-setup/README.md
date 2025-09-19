# Bluetooth Communication Setup with HC-05 Modules

## Current Status

slave
+ADDR:21:13:1FBB5
00:21:13:01:FB:B5

master
+ADDR:21:13:237A9
00:21:13:02:37:A9

## Commands to Set Up HC-05 Modules

To get two HC-05 Bluetooth modules to communicate with each other (one as master, one as slave) for Arduino-to-Arduino communication, follow these steps:

### 1. Enter AT Mode on Both Modules

- Hold the button on the HC-05 while powering it up to enter AT mode (LED blinks slowly).

### 2. Set One HC-05 as Master, the Other as Slave

#### For the Slave Module:

```plaintext
AT+ROLE=0
AT+RESET
```

#### For the Master Module:

```plaintext
AT+ROLE=1
AT+RESET
```

### 3. Find the Slave’s Address (on Slave):

```plaintext
AT+ADDR?
```

- Note the address returned (e.g., `98d3:31:fd3b5c`).

### 4. Set the Master to Pair and Bind to the Slave (on Master):

Replace `98d3,31,fd3b5c` with your slave’s address.

```plaintext
AT+CMODE=1
AT+PAIR=98d3,31,fd3b5c,20
AT+BIND=98d3,31,fd3b5c
AT+LINK=98d3,31,fd3b5c
```

Please keep in mind that you can enter “1” instead of “0” in the “AT+CMODE” command. This option allows the master to connect to any device within its transmission range, rather than being restricted to a specific slave device. If you choose this option, you can skip the second-to-last step; however, be aware that this results in a less secure configuration.

### 5. Connect TX/RX to Arduino

- Connect TX of HC-05 to RX of Arduino, and RX of HC-05 to TX of Arduino (with voltage divider if needed).
