#!/usr/bin/env python3
"""
Module that defins the fucntion filter_dataum -
returns log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message wiath specified fields obfuscated

    Args:
        fields (List[str]):  Fields to obfuscate
        redaction (str): The string to replace the field values with.
        message (str): The log message
        separator (str): The field separator in the log message

    Returns:
        str: The obfuscated log message
    """
    pattern = (f"({'|'.join(re.escape(field) for field in fields)})=.*?"
               f"(?={re.escape(separator)}|$)")
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
