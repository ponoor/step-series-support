"""Messages received from the device."""

import ast
import re
from dataclasses import dataclass as _dataclass
from dataclasses import field, fields
from typing import Any, Callable, Dict, Tuple, TypeVar, Union

# Pylance custom dataclass work around
_T = TypeVar("_T")


def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    return lambda a: a


# Implement a custom dataclass to parse raw strings
@__dataclass_transform__(field_descriptors=(field,))
def dataclass(*args: Tuple[Any], **kwargs: Dict[str, Any]):
    def wrapper(cls):
        cls = _dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            # Concat split string args
            if all([isinstance(x, str) for x in args]):
                args = (" ".join(args),)

            # Break down the args
            if len(args) == 1 and isinstance(args[0], str):
                # First look for custom regex strings
                # These will be <field_name>_re
                all_fields = fields(self)
                for i, field_name in enumerate(f.name for f in all_fields):
                    if field_name.endswith("_re"):
                        match: re.Match = getattr(self, field_name).search(args[0])
                        kwargs[field_name[:-3]] = match[0]
                        args = (
                            (args[0][: match.start()] + args[0][match.end() :]).strip(),
                        )
                args = args[0].split()

                # Now add all to kwargs
                field_names = [
                    f.name
                    for f in all_fields
                    if f.name not in kwargs and not f.name.endswith("_re")
                ]

                # A string in the last field may contain spaces
                if len(args) > len(field_names):
                    last = [f for f in all_fields if f.name == field_names[-1]][0]
                    if last.type in (str, "str"):
                        keep = len(field_names) - 1
                        args = args[:keep] + [" ".join(args[keep:])]
                for i, arg in enumerate(args):
                    field_name = field_names[i]
                    kwargs[field_name] = arg
                args = tuple()
                kwargs.pop("address", None)

            # Remove unnecessary address identifier
            args = list(args)
            if args and args[0] == self.address:
                args.pop(0)

            # Eval positional args
            for i, arg in enumerate(args):
                try:
                    args[i] = ast.literal_eval(arg.capitalize())
                except (AttributeError, ValueError, SyntaxError, NameError):
                    # Catch errors for non-strings, bad strings (i.e. ture instead of true)
                    # or non-evalable strings (i.e. class name)
                    pass

            # Eval named args
            for k, v in kwargs.items():
                try:
                    kwargs[k] = ast.literal_eval(v.capitalize())
                except (AttributeError, ValueError, SyntaxError, NameError):
                    # Catch errors for non-strings, bad strings (i.e. ture instead of true)
                    # or non-evalable strings (i.e. class name)
                    pass

            # Now call the generated dataclass init
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@dataclass
class OSCResponse(object):
    """An abstract class meant to be implemented by OSC resp objects."""

    address: str

