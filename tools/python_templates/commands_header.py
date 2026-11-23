"""Messages to send to the device.

This module provides dataclass objects that act as templates for you to
'fill in' with data. This allows you to focus on WHAT to send, not how.

Some commands will have an extra ``response_cls`` attribute. This
attribute is used internally in the library, but may be useful for you.
It holds the response type, not the actual device response.

All commands that control automatic reporting of the device's internal
state changes have an extra ``callback`` attribute. This attribute is a
shortcut to automatically register a callback to handle incoming
responses from the device.
"""

from dataclasses import asdict, dataclass, field
from typing import Callable, Optional, Tuple, Type

from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder

from stepseries import responses


@dataclass
class OSCCommand(object):
    """An abstract class meant to be implemented by OSC command objects.

    If implementing your own command, it must inherit this class.
    """

    def build(self) -> OscMessage:
        """Converts the builder to a usable OSC message."""
        # Convert the builder to a dictionary
        builder_dict = asdict(self)

        # Extract the values
        # Code is largely copy-paste from pythonosc.UDPClient
        address = builder_dict.pop("address")
        builder_dict.pop("callback", None)
        builder_dict.pop("response_cls", None)

        builder = OscMessageBuilder(address=address)

        # Return as a message string
        for v in builder_dict.values():
            if v is None:
                continue
            if isinstance(v, bool):
                v = int(v)
            builder.add_arg(v)

        return builder.build()

    def stringify(self) -> str:
        """Converts the builder to an OSC message string."""
        # Convert the builder to a dictionary
        builder_dict = asdict(self)
        builder_dict.pop("callback", None)
        builder_dict.pop("response_cls", None)

        # Extract the values
        address: str = builder_dict.pop("address") + " "

        # Return as a message string
        for v in builder_dict.values():
            if isinstance(v, bool):
                v = int(v)
            if v is None:
                continue
            address += str(v) + " "

        return address[:-1]


@dataclass
class OSCSetCommand(OSCCommand):
    """A command that only performs set functions on the device."""


@dataclass
class OSCGetCommand(OSCCommand):
    """A command that only performs get functions on the device."""
