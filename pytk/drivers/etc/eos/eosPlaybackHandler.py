
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .eos import Eos
    from .eosPlaybackTypes import eosCuePendingValidator, eosPlaybackEventValidator, eventTypes


class EosPlaybackHandler:
    def __init__(self, eos: Eos):
        self.eos = eos
        self.pending_cue = None

    async def handle_playback_event(self, event: eosPlaybackEventValidator) -> None:
        """Handle playback events from the Eos device."""

        if event.event_type == eventTypes.CUE_FIRE:
            self.eos.playback.last_cue = self.eos.playback.active_cue if self.eos.playback.active_cue is not None else None
            self.eos.playback.active_cue = event.cue

    async def handle_pending_cue(self, event: eosCuePendingValidator):
        """Handle pending cue events from the Eos device."""
        self.pending_cue = event.cue
