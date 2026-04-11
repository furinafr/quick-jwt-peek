import sys
import json
import base64

def decode_component(component):
    missing_padding = len(component) % 4
    if missing_padding:
        component += "=" * (4 - missing_padding)
    try:
        return json.loads(base64.urlsafe_b64decode(component).decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def peek_jwt(token):
    parts = token.strip().split(".")
    if len(parts) != 3:
        print(json.dumps({"error": "Invalid JWT format: expected 3 dot-separated parts"}, indent=2))
        return

    header = decode_component(parts[0])
    payload = decode_component(parts[1])

    output = {
        "header": header,
        "payload": payload,
        "signature_segment_length": len(parts[2])
    }
    print(json.dumps(output, indent=2))

def main():
    # Allow piping or argument input
    if not sys.stdin.isatty():
        token = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print("Usage: quick-jwt-peek <token> OR echo <token> | quick-jwt-peek")
        sys.exit(1)
    
    if token:
        peek_jwt(token)

if __name__ == "__main__":
    main()