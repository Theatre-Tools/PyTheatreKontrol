from typing import TYPE_CHECKING

from pytk.core.exceptions import InvalidStateError

if TYPE_CHECKING:
    from .eos import Eos
    from .eosPlaybackTypes import (
        eosActiveCueCompletionValidator,
        eosActiveCueValidator,
        eosCuePendingValidator,
        eosPlaybackEventValidator,
        eventTypes,
    )


class EosPlaybackHandler:
    def __init__(self, eos: Eos):
        self.eos = eos

    async def handle_playback_event(
        self,
        event: eosPlaybackEventValidator | eosActiveCueCompletionValidator | eosActiveCueValidator | eosCuePendingValidator,
    ) -> None:
        """Handle playback events from the Eos device."""

        if isinstance(event, eosActiveCueCompletionValidator):
            """Updates the Cue Completion when a new message is received."""
            if event.completion == 1.0:
                self.eos.playback.running = False
            self.eos.playback.completion = event.completion

        elif isinstance(event, eosCuePendingValidator):
            """Update the pending cue value when a new pending cue is received."""
            self.eos.playback.pending_cue = event.cue

        elif isinstance(event, eosPlaybackEventValidator):
            """Update the playback state when a new playback event is received."""
            if event.event_type == eventTypes.CUE_FIRE:
                self.eos.playback.last_cue = self.eos.playback.active_cue
                self.eos.playback.active_cue = event.cue
                self.eos.playback.running = True

            elif event.event_type == eventTypes.CUE_STOP:
                self.eos.playback.stopped = True

            elif event.event_type == eventTypes.CUE_RESUME:
                self.eos.playback.stopped = False

            else:
                raise InvalidStateError(f"Invalid playback event type: {event.event_type}")
