from queue import Queue
from typing import TYPE_CHECKING

from .eos_types import ActiveQueueItem, PendingQueueItem
from .eos_validators import ActiveCompletionValidator, ActiveCueValidator, PendingCueValidator

if TYPE_CHECKING:
    from .eos import EOS


class PendingQueue(Queue):
    def __init__(self) -> None:
        super().__init__()


class ActiveQueue(Queue):
    def __init__(self) -> None:
        super().__init__()

    def update_last_complete(self, completion: float) -> None:
        if self.empty():
            return
        last_item = self.queue[-1]
        last_item.completion = completion

    def completion(self, completion: float) -> None:
        if self.empty():
            raise RuntimeError("No active cues in the queue.")
        last_item = self.queue[-1]
        self.put(ActiveQueueItem(number=last_item.number, list=last_item.list, completion=completion))


class Cues:
    def __init__(self, eos: EOS) -> None:
        self._eos = eos
        self.active_queue = ActiveQueue()
        self.pending_queue = PendingQueue()

    @property
    def active(self) -> ActiveQueueItem | None:
        if self.active_queue.empty():
            return None
        return self.active_queue.queue[-1]

    @property
    def pending(self) -> PendingQueueItem | None:
        if self.pending_queue.empty():
            return None
        return self.pending_queue.queue[-1]

    def active_handler(self, message) -> None:
        if isinstance(message, ActiveCueValidator):
            self.active_queue.put(ActiveQueueItem(number=message.number, list=message.list, completion=message.completion))
        else:
            self.active_queue.completion(message.completion)

    def pending_handler(self, message) -> None:
        self.pending_queue.put(PendingQueueItem(number=message.number, list=message.list, part=message.part))

    def register_handlers(self) -> None:
        try:
            self._eos.instance.register_handler("/eos/out/active/cue/*/*", self.active_handler, validator=ActiveCueValidator)
            self._eos.instance.register_handler(
                "/eos/out/active/cue", self.active_handler, validator=ActiveCompletionValidator
            )
            self._eos.instance.register_handler(
                "/eos/out/pending/cue/*/*", self.pending_handler, validator=PendingCueValidator
            )
            self._eos.instance.register_handler(
                "/eos/out/pending/cue/*/*/*", self.pending_handler, validator=PendingCueValidator
            )
        except Exception as e:
            raise RuntimeError(f"Error registering active cue handler: {e}")
