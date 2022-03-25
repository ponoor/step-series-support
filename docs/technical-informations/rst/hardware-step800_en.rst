*****************
Hardware Overview
*****************

========
PCB size
========

120x80, thickness = 1.6mm

There are five M3 mounting holes on each four corners and in the middle.

|image1| 

Long parts of the top and bottom in this picture are waste
boards, and are removed after the production.

Actual size PDF : `step800_r1_0_0_dimension.pdf`_

======
System
======

The main components are as follows;

+-----------------------+-----------------------+-----------------------+
| Components            | Manufacturer          | Model number          |
+=======================+=======================+=======================+
| MCU                   | Microchip             | `ATSAMD21G18A`_       |
+-----------------------+-----------------------+-----------------------+
| Ethernet Controller   | Wiznet                | `W5500`_              |
+-----------------------+-----------------------+-----------------------+
| Stepper Driver        | STMicroelectronics    | `L6470`_              |
+-----------------------+-----------------------+-----------------------+
| DC-DC Converter       | CUI                   | `P78E05-1000`_        |
+-----------------------+-----------------------+-----------------------+

===============
Pin assignments
===============

======== ===================== =============================
pin      function              etc
======== ===================== =============================
D0       Shift Register SCK    
D1       NC                    Pad exposed in soldering side
D2       Shift Register MOSI   
D3       Shift Register MISO   
D4       SD_CS                 
D5       Shift Register ENABLE 
D6       L6470 MISO            
D7       NC                    Pad exposed in soldering side
D8       NC                    Pad exposed in soldering side
D9       NC                    Pad exposed in soldering side
D10      W5500_CS              
D11      L6470 MOSI            
D12      L6470 SCK             
D13      L                     
D20/SDA  NC                    Pad exposed in soldering side
D21/SCL  NC                    Pad exposed in soldering side
D22/MISO W5500_MISO            
D23/MOSI W5500_MOSI            
D24/SCK  W5500_SCK             
D30      NC                    
D31      NC                    
D38      NC                    Pad exposed in soldering side
A0       L6470_CS              
A1       NC                    Pad exposed in soldering side
A2       L6470_RESET           
A3       W5500_RESET           
A4       SD_DETECT             
A5       Shift Register CS     
======== ===================== =============================

Since the L6470_RESET and W5500_RESET are connected to the reset pins of
L6470 and W5500 individually, be sure to set pinMode to OUTPUT and then
set the state to HIGH.

=====================
Pads on PCB rear side
=====================

There are unassigned pins and power pads on the rear side of PCB. They
are 2.54mm picth, so you can attach surface-mount pin-headers and IC
sockets. R6 and R7 on the rear side can be used for the pull-up for the
i2c pins(SDA, SDL). The chip size is 1608(0603).

Since these pins are not controlled from firmware, customizing firmware
for your own purpose is necessary.

.. image:: https://ponoor.com/cms/wp-content/uploads/2021/09/step800_reserved_pads.jpg

**************
SPI assignment
**************

For the STEP800, different SPI ports are used for the L6470 and W5500
for the ease of firmware process. Here is a very informative guide to
SPI allocation in ATSAMD21.

https://learn.adafruit.com/using-atsamd21-sercom-to-add-more-spi-i2c-serial-ports

=====
W5500
=====

======== ======== ====== ==========
Pin      Function SERCOM SERCOM Alt
======== ======== ====== ==========
D22/MISO MISO     -      SERCOM4.0
D23/MOSI MOSI     -      SERCOM4.2
D24/SCK  SCK      -      SERCOM4.3
======== ======== ====== ==========

=====
L6470
=====

=== ======== ====== ==========
Pin Function SERCOM SERCOM Alt
=== ======== ====== ==========
D6  MISO     -      SERCOM3.2
D11 MOSI     -      SERCOM3.0
D12 SCK      -      SERCOM3.3
=== ======== ====== ==========

==========================================
Shift registers (DIP switch, brake output)
==========================================

=== ======== ========= ==========
Pin Function SERCOM    SERCOM Alt
=== ======== ========= ==========
D3  MISO     -         SERCOM2.1
D2  MOSI     SERCOM2.2 -
D0  SCK      -         SERCOM2.3
=== ======== ========= ==========

.. _l6470-1:

*****
L6470
*****

=====
Clock
=====

A 16MHz crystal oscillator is connected to the OSCIN of Motor ID 1’s
L6470. From there, OSCOUT and OSCIN are daisy chained in order of IDs,
so please set each L6470 to “External 16MHz input, Inverted
output(``EXT_16MHZ_OSCOUT_INVERT``)”. If the internal clock is used, the
movement may shift gradually during constant speed operation.

*****************************************************
Unavailable L6470 features due to the hardware design
*****************************************************

====
STCK
====

Since it is not wired, Step Clock operation is not possible.

=====
ADCIN
=====

This is directly wired with GND and can not use.

.. _step800_r1_0_0_dimension.pdf: https://ponoor.com/cms/wp-content/uploads/2021/09/step800_r1_0_0_dimension.pdf
.. _ATSAMD21G18A: https://www.microchip.com/wwwproducts/en/ATsamd21g18
.. _W5500: https://www.wiznet.io/product-item/w5500/
.. _L6470: https://www.st.com/en/motor-drivers/L6470.html
.. _P78E05-1000: https://www.jp.cui.com/product/dc-dc-converters/non-isolated/p78e-1000-series

.. |image1| image:: https://ponoor.com/cms/wp-content/uploads/2021/09/step800_r1_0_0_dimension-1.png
