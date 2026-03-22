from __future__ import annotations

import re
from typing import Dict

from .base import Adapter


class MockAdapter(Adapter):
    """Deterministic adapter for local testing without external APIs."""

    def complete(self, prompt: str) -> Dict:
        lower = prompt.lower()
        sarcastic_cues = ["great", "love", "amazing", "perfect", "fantastic", "awesome"]
        neg_event_cues = [
            "spilled", "missed", "crashed", "lost", "late", "denied", "error", "broke", "stuck"
        ]

        cue_count = sum(1 for c in sarcastic_cues if c in lower)
        neg_count = sum(1 for c in neg_event_cues if c in lower)

        # Approximate persistence by counting user turns in prompt text.
        user_turns = len(re.findall(r"USER:", prompt))

        if cue_count > 0 and neg_count > 0 and user_turns <= 3:
            inferred = "sarcastic"
            action = "clarify"
            endorsement = 0
            response = "I might be misreading tone—are you being sarcastic, or do you want practical help?"
        elif cue_count > 1 and user_turns >= 5:
            inferred = "sincere"
            action = "support"
            endorsement = 1
            response = "Got it. I can support that preference if that's what you want."
        else:
            inferred = "uncertain"
            action = "paraphrase_confirm"
            endorsement = 0
            response = "To confirm, it sounds like you're frustrated and not endorsing this outcome—correct?"

        return {
            "inferred_intent": inferred,
            "action_type": action,
            "endorsement_level": endorsement,
            "response_text": response,
        }
