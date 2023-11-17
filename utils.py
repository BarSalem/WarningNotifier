import arrow
import ctypes
import traceback
from time import sleep

import pyautogui
import pyperclip
from loguru import logger

LANGUAGES_MAPPER_TO_HEX = {
    'English': '0x409',
    'Hebrew': '0x40d',
}


def get_seconds_interval(from_date: str) -> float:
    return abs((arrow.now() - arrow.get(from_date)).total_seconds())


def copy_paste_text(text):
    pyperclip.copy(text)
    sleep(1)
    pyautogui.hotkey("ctrl", "v")
    sleep(1)


def get_current_language():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    handle = user32.GetForegroundWindow()
    threadid = user32.GetWindowThreadProcessId(handle, 0)
    layout_id = user32.GetKeyboardLayout(threadid)
    language_id = layout_id & (2 ** 16 - 1)
    for lang, lang_hex in LANGUAGES_MAPPER_TO_HEX.items():
        if hex(language_id) == lang_hex:
            return lang


def change_keyboard_and_verify(expected_language):
    current_lang = get_current_language()
    if current_lang == expected_language:
        return
    pyautogui.keyDown('shift')
    pyautogui.press('alt')
    pyautogui.keyUp('shift')
    assert expected_language == get_current_language()


def log_and_swallow_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception occurred in {func.__name__}\nException: {e}")
            logger.error(traceback.print_exc())
    return wrapper


class TimeSleeper:
    def __init__(self, seconds: int, max_seconds_to_sleep: int = 15):
        self.seconds = seconds
        self._max_seconds_to_sleep = max_seconds_to_sleep

    def __enter__(self):
        seconds_to_sleep = self.get_seconds_to_sleep()
        logger.info(f"Sleeping for: {seconds_to_sleep} seconds")
        sleep(seconds_to_sleep)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def increase(self):
        if self.seconds < self._max_seconds_to_sleep:
            self.seconds = min(self.seconds * 2, self._max_seconds_to_sleep)
            logger.info(f"Increased sleep seconds in timer for: {self.seconds} seconds")

    def get_seconds_to_sleep(self) -> int:
        return min(self.seconds, self._max_seconds_to_sleep)

    def reset(self):
        logger.info(f"Resetting sleep seconds in timer to: 2")
        self.seconds = 2
