#!/usr/bin/env python3
import re
from typing import List
""" module that defins the fucntion filter_dataum -
returns log message obfuscated
"""


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str):
    """
    Returns the log message wiath specified fields obfuscated

    Args:
        fields (List[str]):  Fields to obfuscate
        redaction (str): The string to prelace the field values with.
        message (str): The log message
        separator (str): The field separator in the log message

    Returns:
        str: The obfuscated log message
    """
    pattern = (f"({'|'.join(re.escape(field) for field in fields)})=.*?"
               f"(?={re.escape(seperator)}|$)")
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
