import sys
import json
import base64
from typing import Dict, Any, Union, Optional, List, Final
from dataclasses import dataclass, asdict, field

class JWTError(Exception): """Base exception for JWT operations."""

class InvalidTokenFormat(JWTError): """Raised when token does not follow header.payload.signature format."""

@dataclass(frozen=True)
class JWTPreview:
    header: Dict[str, Any]
    payload: Dict[str, Any]
    signature_length: int
    valid: bool = True
    errors: List[str] = field(default_factory=list)

class JWTDecoder:
    """Stateless decoder for JWT segments."""
    
    PADDING_CHAR: Final[str] = "="

    @staticmethod
    def _pad_segment(segment: str) -> str:
        """Calculates and appends necessary base64 padding."""
        return segment + (JWTDecoder.PADDING_CHAR * (-len(segment) % 4))

    @classmethod
    def decode_segment(cls, segment: str) -> Dict[str, Any]:
        """Decodes URL-safe base64 encoded JSON string."""
        try:
            padded = cls._pad_segment(segment)
            decoded_bytes = base64.urlsafe_b64decode(padded)
            return json.loads(decoded_bytes.decode("utf-8"))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
            raise JWTError(f"Segment decoding failed: {str(e)}") from e

    @classmethod
    def inspect(cls, token: str) -> JWTPreview:
        """Parses token into a JWTPreview model, capturing internal errors."""
        parts = token.strip().split(".")
        if len(parts) != 3:
            return JWTPreview({}, {}, 0, False, ["Invalid format: expected 3 parts"])

        errors: List[str] = []
        header = {}
        payload = {}

        try:
            header = cls.decode_segment(parts[0])
        except JWTError as e:
            errors.append(f"Header Error: {str(e)}")

        try:
            payload = cls.decode_segment(parts[1])
        except JWTError as e:
            errors.append(f"Payload Error: {str(e)}")

        return JWTPreview(
            header=header,
            payload=payload,
            signature_length=len(parts[2]),
            valid=not errors,
            errors=errors
        )

class CLIHandler:
    """Manages CLI interactions and I/O streams."""

    @staticmethod
    def _get_raw_input() -> Optional[str]:
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        return sys.argv[1] if len(sys.argv) > 1 else None

    @classmethod
    def run(cls) -> None:
        try:
            token = cls._get_raw_input()
            if not token:
                print("Usage: jwt-peek <token> OR echo <token> | jwt-peek", file=sys.stderr)
                sys.exit(64)

            preview = JWTDecoder.inspect(token)
            output = json.dumps(asdict(preview), indent=2)
            
            # Handle potential broken pipes (e.g., piping to 'head')
            try:
                sys.stdout.write(output + "\n")
            except BrokenPipeError:
                devnull = os.open(os.devnull, os.O_WRONLY)
                os.dup2(devnull, sys.stdout.fileno())
                sys.exit(1)

        except Exception as e:
            print(json.dumps({"error": "Internal failure", "details": str(e)}), file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    CLIHandler.run()