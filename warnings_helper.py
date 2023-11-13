from collections import defaultdict

import arrow
import requests

from globals import MESSAGES_INTERVAL
from utils import log_and_swallow_exceptions, get_seconds_interval

WARNINGS_URL = "https://www.oref.org.il/WarningMessages/History/AlertsHistory.json"
WARNING_KORE_URL = "https://www.kore.co.il/redAlert.json"


class MessagesKeys:
    CITY = 'data'
    WARNING_TYPE = 'title'
    DATE = 'alertDate'


class WarningsHelper:
    def __init__(self):
        self.url = WARNINGS_URL

    @log_and_swallow_exceptions
    def get_warnings(self) -> list:
        return requests.get(self.url).json()

    def get_sorted_warnings(self) -> list:
        warnings = self.get_warnings() or []
        return sorted(warnings, key=lambda warning: arrow.get(warning['alertDate']), reverse=True)

    def get_sorted_warnings_since(self, seconds_interval: int) -> list:
        """
        :param seconds_interval: should be in the following format "YYYY-MM-DD HH:MM:SS"
        :return: list
        """
        def is_in_interval(warning: dict) -> bool:
            warning_arrow_obj = arrow.get(warning['alertDate']).replace(tzinfo="+02:00")
            return abs((current_ts - warning_arrow_obj).total_seconds()) <= seconds_interval

        current_ts = arrow.now()
        warnings = self.get_sorted_warnings()
        return list(filter(lambda warning: is_in_interval(warning), warnings))

    def get_warnings_by_city(self, cities: list, since: arrow = None) -> list[dict]:
        warnings = self.get_sorted_warnings_since(since) if since else self.get_sorted_warnings()
        return list(filter(lambda item: item[MessagesKeys.CITY] in cities, warnings))

    @classmethod
    def get_warning_message_by_cities(cls, warnings: list[dict]) -> str:
        return ''.join([f"{warning[MessagesKeys.CITY]} {warning[MessagesKeys.WARNING_TYPE]} "
                        f"{warning[MessagesKeys.DATE]}\n" for warning in warnings])


class MessagesHistory:
    MESSAGES = defaultdict(lambda: [])

    @classmethod
    def add_messages(cls, messages: list[dict]) -> None:
        for message in messages:
            if message[MessagesKeys.CITY] not in cls.MESSAGES[message[MessagesKeys.DATE]]:
                cls.MESSAGES[message[MessagesKeys.DATE]].extend([message[MessagesKeys.CITY]])

    @classmethod
    def is_message_in_history(cls, message_obj: dict) -> bool:
        return message_obj[MessagesKeys.CITY] in cls.MESSAGES[message_obj[MessagesKeys.DATE]]

    @classmethod
    def clear_messages(cls) -> None:
        cls.MESSAGES = (
                {ts: ts_cities for ts, ts_cities in cls.MESSAGES.items() if get_seconds_interval(ts) < MESSAGES_INTERVAL}
                or
                defaultdict(lambda: [])
        )
