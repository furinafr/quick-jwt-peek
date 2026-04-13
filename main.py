import sys
import json
import base64
from typing import Dict, Any, Union, Optional
from dataclasses import dataclass, asdict

@dataclass
class JWTPreview:
    header: Dict[str, Any]
    payload: Dict[str, Any]
    signature_length: int
    valid_format: bool = True

class JWTDecoder:
    @staticmethod
    def _add_padding(segment: str) -> str:
        """Ensures base64 string has correct padding."""
        return segment + "=" * (-len(segment) % 4)

    @classmethod
    def decode_segment(cls, segment: str) -> Dict[str, Any]:
        """
        Decodes a single JWT segment (header or payload).
        Returns a dictionary or an error descriptor.
        """
        try:
            padded = cls._add_padding(segment)
            decoded_bytes = base64.urlsafe_b64decode(padded)
            return json.loads(decoded_bytes.decode("utf-8"))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
            return {"error": f"Failed to decode segment: {str(e)}"}

    @classmethod
    def inspect(cls, token: str) -> Union[JWTPreview, Dict[str, str]]:
        """
        Parses a JWT string into a structured preview without verification.
        """
        parts = token.strip().split(".")
        if len(parts) != 3:
            return {"error": "Invalid JWT format: expected 3 dot-separated parts"}

        return JWTPreview(
            header=cls.decode_segment(parts[0]),
            payload=cls.decode_segment(parts[1]),
            signature_length=len(parts[2])
        )

class CLIHandler:
    @staticmethod
    def get_input() -> Optional[str]:
        """Handles input from stdin or CLI arguments."""
        if not sys.stdin.isatty():
            return sys.stdin.read().strip()
        if len(sys.argv) > 1:
            return sys.argv[1]
        return None

    @staticmethod
    def run() -> None:
        token = CLIHandler.get_input()
        if not token:
            print("Usage: jwt-peek <token> OR echo <token> | jwt-peek", file=sys.stderr)
            sys.exit(1)

        result = JWTDecoder.inspect(token)
        output = asdict(result) if isinstance(result, JWTPreview) else result
        print(json.dumps(output, indent=2))

if __name__ == "__main__":
    CLIHandler.run()