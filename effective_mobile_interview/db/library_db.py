from effective_mobile_interview.core.settings import get_settings
from effective_mobile_lib.db.db import DB


class LibraryDB(DB):
    def __init__(self, storage_filepath):
        super().__init__(storage_filepath)

    def ensure_indexes(self):
        return super().ensure_indexes()

db = LibraryDB(get_settings().storage_filepath)
