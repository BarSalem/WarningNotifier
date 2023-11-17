import webbrowser
from time import sleep

import pyautogui
from loguru import logger

from chrome import close_all_chrome_open_tabs
from globals import WHATS_APP_GROUP_ID
from utils import log_and_swallow_exceptions, copy_paste_text


class WhatsAppHelper:

    def __init__(self,
                 group_id: str = WHATS_APP_GROUP_ID,
                 wait_time: int = 8,
                 close_time: int = 2):
        self.group_id = group_id
        self.wait_time = wait_time
        self.close_time = close_time

    def open_whats_app_group(self):
        url = f"https://web.whatsapp.com/accept?code={self.group_id}"
        webbrowser.get("windows-default").open(url)
        sleep(self.wait_time)

    @log_and_swallow_exceptions
    def send_message(self, message):
        self.open_whats_app_group()
        logger.info(f"Sending message WhatsApp message to group with ID: {self.group_id}")
        copy_paste_text(message)
        pyautogui.press('enter')
        logger.info(f"Successfully sent WhatsApp message to group with ID: {self.group_id}")

    def send_message_and_close_all_tabs(self, message):
        self.send_message(message)
        sleep(self.close_time)
        close_all_chrome_open_tabs()
