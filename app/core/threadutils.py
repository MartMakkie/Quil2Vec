from PySide6.QtCore import QObject, QThread, Signal, Slot
import traceback

class FunctionWorker(QObject):
    finished = Signal(object)  # result
    error = Signal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception:
            tb = traceback.format_exc()
            self.error.emit(tb)
class Worker(QObject):
    
    finished = Signal()
    result = Signal(object)
    error = Signal(Exception)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    # def run(self):
    #     try:
    #         print("[Worker] Starting function in thread...")
    #         result = self.fn(*self.args, **self.kwargs)
    #         print("[Worker] Function completed.")
    #         self.result.emit(result)
    #     except Exception as e:
    #         print(f"[Worker] Error occurred: {e}")
    #         self.error.emit(e)
    #     finally:
    #         self.finished.emit()
    def run(self):
        print("[Worker] run() called")
        try:
            result = self.fn(*self.args, **self.kwargs)
            print("[Worker] fn() completed")
            self.result.emit(result)
        except Exception as e:
            print(f"[Worker] Error: {e}")
            self.error.emit(e)
        finally:
            print("[Worker] Finished signal emitted")
            self.finished.emit()