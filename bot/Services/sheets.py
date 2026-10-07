import logging
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

from bot.config import config

logger = logging.getLogger(__name__)

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


class SheetsService:
    """Обёртка над Google Sheets для работы со списком ДР."""

    def __init__(self) -> None:
        self._client: gspread.Client | None = None
        self._sheet: gspread.Worksheet | None = None
        self._connect()

    def _connect(self) -> None:
        try:
            creds = Credentials.from_service_account_file(
                config.GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
            )
            self._client = gspread.authorize(creds)
            self._sheet = self._client.open(config.SPREADSHEET_NAME).worksheet(config.SHEET_NAME)
            logger.info("Подключение к Google Sheets установлено.")
        except Exception as e:
            logger.exception("Ошибка подключения к Google Sheets: %s", e)
            raise

    @property
    def sheet(self) -> gspread.Worksheet:
        if self._sheet is None:
            self._connect()
        assert self._sheet is not None
        return self._sheet

    def get_all(self) -> list[dict[str, Any]]:
        return self.sheet.get_all_records()

    def add(self, name: str, date_str: str, extra: str = "") -> None:
        self.sheet.append_row([name, date_str, extra], value_input_option="USER_ENTERED")

    def delete(self, name: str) -> bool:
        try:
            cell = self.sheet.find(name, in_column=1)
        except gspread.exceptions.CellNotFound:
            return False
        if cell is None:
            return False
        self.sheet.delete_rows(cell.row)
        return True


sheets_service = SheetsService()
