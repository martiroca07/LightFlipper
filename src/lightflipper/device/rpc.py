from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass
class RPCRequest:
    command: str
    payload: dict[str, Any] = field(default_factory=dict)
    request_id: str = "0"

    def validate(self) -> str | None:
        if not self.command or not str(self.command).strip():
            return "RPC command is required."
        return None


class _MockRPCTransport:
    """Simple in-memory transport used for regression-safe command validation."""

    def send(self, request: RPCRequest) -> dict[str, Any]:
        return {
            "status": "ok",
            "command": request.command,
            "payload": dict(request.payload or {}),
            "request_id": request.request_id,
        }


class FlipperRPCClient:
    """Minimal transport-agnostic RPC client for Flipper-style commands."""

    def __init__(self, transport: Any | None = None) -> None:
        self.transport = transport or _MockRPCTransport()

    def send_command(self, command: str, payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
        request = RPCRequest(
            command=str(command or "").strip(),
            payload=dict(payload or {}),
            request_id="rpc-1",
        )
        error = request.validate()
        if error:
            return {"status": "error", "error": error}

        try:
            response = self.transport.send(request)
        except Exception as exc:  # pragma: no cover - transport-specific exceptions
            return {"status": "error", "error": f"RPC transport failed: {exc}"}

        normalized = {
            "status": response.get("status", "ok"),
            "command": request.command,
            "payload": dict(response.get("payload", request.payload)),
            "request_id": response.get("request_id", request.request_id),
        }
        if response.get("status") == "error":
            normalized["error"] = response.get("error", "RPC command failed.")
        return normalized
