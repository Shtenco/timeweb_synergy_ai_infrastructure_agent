"""An allowlisted dry-run planner; it never executes host or cloud actions."""

from __future__ import annotations

import shlex


def propose_action(command: str, allowlist: set[str] | frozenset[str]) -> dict:
    if not isinstance(command, str) or not command.strip():
        raise ValueError("command must be a nonempty string")
    normalized = " ".join(shlex.split(command.strip().lower()))
    allowed_commands = {" ".join(shlex.split(item.strip().lower())) for item in allowlist}
    allowed = normalized in allowed_commands
    return {
        "requested_action": command,
        "normalized_action": normalized,
        "allowed": allowed,
        "executed": False,
        "decision": "proposed_for_human_review" if allowed else "rejected_not_allowlisted",
    }


def run(seed: int = 42) -> dict:
    allowlist = {"restart api", "read status api", "tail logs api"}
    return {
        "evidence_type": "simulation",
        "seed": seed,
        "actions": [
            propose_action("restart api", allowlist),
            propose_action("delete database", allowlist),
            propose_action("restart api; delete database", allowlist),
        ],
        "limitations": [
            "No host, server, shell, or cloud API is called.",
            "An allowlist decision does not establish that an action is safe in a real environment.",
        ],
    }
