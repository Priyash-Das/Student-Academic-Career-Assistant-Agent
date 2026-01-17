from study_buddy.config.settings import (
    STATUS_READY,
    STATUS_PROCESSING,
    STATUS_COMPLETED,
    STATUS_ERROR,
)
class StatusManager:
    def __init__(self, callback=None):
        self._status = STATUS_READY
        self._callback = callback
    def set(self, status: str):
        self._status = status
        if self._callback:
            self._callback(status)
    def ready(self):
        self.set(STATUS_READY)
    def processing(self):
        self.set(STATUS_PROCESSING)
    def completed(self):
        self.set(STATUS_COMPLETED)
    def error(self):
        self.set(STATUS_ERROR)
    @property
    def current(self):
        return self._status