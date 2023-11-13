import pygetwindow as gw
import pyautogui

from loguru import logger


def get_chrome_window_title():
    return gw.getWindowsWithTitle("Google Chrome")


def close_all_chrome_open_tabs():
    chrome_window = get_chrome_window_title()
    while chrome_window:
        chrome_window[0].activate()
        pyautogui.hotkey("ctrl", "w")
        chrome_window = get_chrome_window_title()
    logger.info("Successfully closed all Chrome tabs")
