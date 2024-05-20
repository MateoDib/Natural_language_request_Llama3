"""
clipboard_utils.py

This module provides utility functions for interacting with the system clipboard.

Functions:
    - detect_clipboard_method(): Retrieve OS to choose a clipboard management method.
    - get_clipboard(): Retrieves text content from the system clipboard.
    - copy_to_clipboard(text: str): Copies text content to the system clipboard.
"""

import sys
import subprocess
import pyperclip

def detect_clipboard_method():
    """
    Detect the appropriate clipboard method based on the operating system.

    Returns:
        str: The clipboard method ('xsel', 'pyperclip', or 'unsupported').
    """
    platform = sys.platform
    if platform == "darwin":
        return "pyperclip"
    if platform.startswith("linux"):
        return "xsel"
    print(f"Warning: {platform} might not be supported")
    return "unsupported"

def get_clipboard():
    """
    Retrieve text content from the system clipboard.

    Returns:
        str: The text content retrieved from the clipboard.
    """
    method = detect_clipboard_method()
    if method == "xsel":
        result = subprocess.run(['xsel', '--clipboard', '--output'],
                                stdout=subprocess.PIPE, check=True)
        return result.stdout.decode('utf-8')
    if method == "pyperclip":
        return pyperclip.paste()
    print("Unsupported platform")
    return ""

def copy_to_clipboard(text):
    """
    Copy text content to the system clipboard.

    Args:
        text (str): The text content to be copied to the clipboard.
    """
    method = detect_clipboard_method()
    if method == "xsel":
        with subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE) as process:
            process.communicate(input=text.encode('utf-8'))
    elif method == "pyperclip":
        pyperclip.copy(text)
    else:
        print("Unsupported platform")
