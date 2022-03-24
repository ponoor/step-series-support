========================
Stepper motor and homing
========================

When the system powers up, it doesn’t know where the motor is currently
positioned. It could be pointing to various directions depending on the
timing of the last time the system was shut off.

Also, if the stepper motor receives exceeding external force, the step
will slip out of alignment (**stall**). If this happens, the motor will
continue to work with offset between the programmed and its physical
position.

Therefore, applications that have position or orientation must use
sensors to detect a reference position on startup or periodically. This
action is called **homing**.

=================
Sensor and switch
=================

.. figure:: http://ponoor.com/manage/wp-content/uploads/2020/10/two-homing-sensors.png
   :alt: Two configuration of homing sensor

   Two configuration of homing sensor

Photointerrupters are often used as home sensors. On the left, a white
piece of plastic attached to the slider blocks the photointerrupter’s
light-emitting and receiving parts. The right side is an example of a
rotary table, where the photo interrupter responds to the black screw.

Other devices such as microswitches, or photoelectric sensors are also
used for the sensing.

============================
HOME sensor and LIMIT sensor
============================

Each axis of STEP400/STEP800 has HOME connector which can connect
sensors or switches. STEP400 has LIMIT sensor inputs in addition to HOME
inputs. 5V is supplied to each connector for the sensing power source.

----
HOME
----

This input is connected directly to the motor driver chip and can be
used in conjunction with the driver’s homing function. Usually, this
connector is used for the home sensor.

-----------------------
LIMIT (Only in STEP400)
-----------------------

Some applications may require two sensors. For example, a slider has a
limited operating range, and if it stalls during the operation, it may
collide with one of either end. In such cases, installing sensors on
both ends of the slider will prevent collisions.

The motor can be set to force-stop when these sensors respond, but these
can also be used as simple switch inputs separated from the motor
operation. For example, you can connect a push button to one of them and
press to send an OSC message.

----------------------------
Collision prevention setting
----------------------------

You can limit the motor rotate direction when HOME or LIMIT sensors are
active. With the
command `/setProhibitMotionOnHomeSw`_ and `/setProhibitMotionOnLimitSw`_ you
can prohibit the actuator to move towards ``homingDirection`` when the
HOME sensor is active, or the reverse direction
towards ``homingDirection`` when the LIMIT sensor is active. With
this, you can prevent mechanism from collision.

``homingDirection`` can be set from `/setHomingDirection`_ or
from the configTool. This setting is also used for following `/homing`_
command.

.. figure:: https://ponoor.com/cms/wp-content/uploads/2020/08/homingDirection-800x533.jpg
   :alt: Homing Direction

   Homing Direction

===============
Homing commands
===============

The homing command in the STEP400 system is\ ```/homing```_. This
command consists from two commands, ``/goUntil``\ and\ ``/releaseSw``
which are inherited from the Motor Driver Chip PowerSTEP01. Let’s look
closer to those commands.

------------
``/goUnitl``
------------

First, use this command to move towards the home sensor. The motor will
decelerate and then stop when the home sensor reacts (if it has been set
up as such). -> ```/goUntil```_

--------------
``/releaseSw``
--------------

The position where the motor stops is the origin / home position!
However, strictly speaking, the ``/goUnitl`` command does not stop
immediately, but stop after deceleration, so it’s current position has
negative offset from the point where the sensor have actually responded.
This command slowly moves in the opposite direction from the current
position and stops immediately when the sensor reading is no longer
positive. -> ```/releaseSw```_

Both commands can be set to reset the current position to zero on the
moment when the sensor responds. -> ```/setHomeSwMode```_

See this video for these commands in operation.

.. container:: embed-video

   .. raw:: html

      <iframe width="560" height="315" src="https://www.youtube.com/embed/AydxbL6-a_g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>

   .. raw:: html

      </iframe>

-----------
``/homing``
-----------

It is possible to send above two commands over OSC one after another,
the\ ```/homing```_ command executes this sequence in single operation.
It will automatically complete the home sequence according to the homing
direction and homing speed which are pre-configured from the configTool
or over OSC commands.

--------
Time-out
--------

The time-out duration can be set for each of
``/goUntil``\ and\ ``/releaseSw`` commands. The controller will halts
the actuator movement as the Time-out, if no change in the sensor
reading is detected within this time frame. This is to prevent the
moving part to be pushed against other mechanical object endlessly, by
giving up the homing sequence and stops at the specified timing.

============================
Normal open and Normal close
============================

---------------------
Electrical connection
---------------------

Let’s determine the “sensor reaction” a little more in detail. The pin
assignments of HOME and LIMIT connectors are as follows.

========== ===================
Pin number Function
========== ===================
1          GND
2          Switch/Sensor input
3          5V Power Output
========== ===================

Each sensor pin on HOME and LIMIT is pulled up to 3.3V. To connect the
switch, connect the GND (#1) and the sensor terminal (#2). When the
switch is pressed, it is connected to the GND pin and the voltage drops
from 3.3V to 0V. When the voltage changes from HIGH level to LOW level
(a.k.a. **Falling Edge**), the sensor is considered to have responded.

Let’s take an photo interrupter `EE-SX671A`_ as an example, where the
connection is as follows:

.. figure:: http://ponoor.com/manage/wp-content/uploads/2020/10/ee-sx67.jpeg
   :alt: EE-SX671A Diagram

   EE-SX671A Diagram

========== =================== ==========
Pin number Function            Sensor pin
========== =================== ==========
1          GND                 -
2          Switch/Sensor input OUT
3          5V Power Output     +
========== =================== ==========

==================================================================
Whether light should enter or be blocked upon the sensor detection
==================================================================

This is the part you need to consider carefully before ordering a
sensor.

.. figure:: http://ponoor.com/manage/wp-content/uploads/2020/10/sensor_dark_light.png
   :alt: Dark on or Light on

   Dark on or Light on

In the case of the left picture, the light enters into the sensor at the
home position, but in the picture on the right, the light is blocked at
the home position.

There are two types of sensors, one that turns on when light enters and
one that turns on when light is interrupted. In the case of the above
Omron sensor, the action is toggled by connecting “L” and “+” terminals.

The mechanism and sensor must be combined in such a way that the sensor
pin goes from HIGH to LOW at the home position.

=================
For rotary tables
=================

In the example on the picture above left, the response position of the
home sensor will differ between clockwise and counterclockwise,
depending on the size of the hole. The STEP400 can notify both HIGH to
LOW and LOW to HIGH changes of the home sensor by OSC messages. The
message also includes the rotation direction, so you can align the home
position if you write a conditional sequence for each rotation
direction. -> ```/enableHomeSwReport```_

.. _/setProhibitMotionOnHomeSw: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononhomesw_intmotorid_boolenable
.. _/setProhibitMotionOnLimitSw: https://ponoor.com/en/docs/step-series/osc-command-reference/alarm-settings/#setprohibitmotiononlimitsw_intmotorid_boolenable
.. _/setHomingDirection: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#sethomingdirection_intmotorid_booldirection
.. _/homing: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#homing_intmotorid
.. _``/goUntil``: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#gountil_intmotorid_boolact_floatspeed
.. _``/releaseSw``: https://ponoor.com/en/docs/step-series/osc-command-reference/homing/#releasesw_intmotorid_boolact_booldir
.. _``/setHomeSwMode``: https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#sethomeswmode_intmotorid_boolsw_mode
.. _EE-SX671A: http://www.ia.omron.com/product/item/2219/
.. _``/enableHomeSwReport``: https://ponoor.com/en/docs/step-series/osc-command-reference/home-limit-sensors/#enablehomeswreport_intmotorid_boolenable
