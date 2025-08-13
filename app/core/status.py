from PySide6.QtCore import QObject, Signal
import logging


class StatusEmitter(QObject):
    newMessage = Signal(str)

class StatusBarHandler(logging.Handler):
    def __init__(self, signal_emitter):
        super().__init__()
        self.signal_emitter = signal_emitter  # A QObject that has newMessage signal

    def emit(self, record):
        msg = self.format(record)
        self.signal_emitter.newMessage.emit(msg)