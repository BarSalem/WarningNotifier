import arrow
from loguru import logger

from globals import MESSAGES_INTERVAL
from utils import TimeSleeper
from warnings_helper import WarningsHelper, MessagesHistory
from whats_app import WhatsAppHelper


WARNINGS_INSTANCE = WarningsHelper()
WHATS_APP_INSTANCE = WhatsAppHelper()
TIME_SLEEPER = TimeSleeper(2)
CITIES_LIST = ['כיסופים']


while True:
    with TIME_SLEEPER as time_sleeper:
        warnings = WARNINGS_INSTANCE.get_sorted_warnings_since(seconds_interval=MESSAGES_INTERVAL)
        if warnings:
            filtered_warnings = [warning for warning in warnings if not MessagesHistory.is_message_in_history(warning)]
            if filtered_warnings:
                warnings_message = WARNINGS_INSTANCE.get_warning_message_by_cities(filtered_warnings)
                WHATS_APP_INSTANCE.send_message_and_close_all_tabs(warnings_message)
                MessagesHistory.add_messages(filtered_warnings)
                time_sleeper.reset()
            else:
                time_sleeper.increase()
        else:
            logger.info(f"Could not find any warning in the last {MESSAGES_INTERVAL//60} minutes")
            time_sleeper.increase()
            MessagesHistory.clear_messages()
