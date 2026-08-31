from typing import TYPE_CHECKING

from pyosc import OSCMessage

from pytk.core.exceptions import InvalidStateError

from .eosPlaybackTypes import (
    eosActiveCueCompletionValidator,
    eosActiveCueValidator,
    eosCuePendingValidator,
    eosPlaybackEventValidator,
    eventTypes,
)

if TYPE_CHECKING:
    from .eos import Eos


class eosPlaybackHandler:
    def __init__(self, eos: Eos):
        self.eos = eos

    def handle_playback_event(
        self,
        message: eosPlaybackEventValidator
        | eosActiveCueCompletionValidator
        | eosActiveCueValidator
        | eosCuePendingValidator
        | OSCMessage,
    ) -> None:
        """Handle playback events from the Eos device."""

        if isinstance(message, eosActiveCueCompletionValidator):
            """Updates the Cue Completion when a new message is received."""
            if message.completion == 1.0:
                self.eos.playback.running = False
            self.eos.playback.completion = message.completion

        elif isinstance(message, eosCuePendingValidator):
            """Update the pending cue value when a new pending cue is received."""
            self.eos.playback.pending_cue = message.cue

        elif isinstance(message, eosPlaybackEventValidator):
            """Update the playback state when a new playback event is received."""
            if message.event_type == eventTypes.CUE_FIRE:
                self.eos.playback.last_cue = self.eos.playback.active_cue
                self.eos.playback.active_cue = message.cue
                self.eos.playback.running = True

            elif message.event_type == eventTypes.CUE_STOP:
                self.eos.playback.stopped = True

            elif message.event_type == eventTypes.CUE_RESUME:
                self.eos.playback.stopped = False

            else:
                raise InvalidStateError(f"Invalid playback event type: {message.event_type}")
        else:
            raise InvalidStateError(f"Invalid playback event message type: {type(message)}")
