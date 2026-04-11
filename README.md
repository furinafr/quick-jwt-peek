# Quick JWT Peek

Inspect the contents of a JSON Web Token (JWT) directly from your terminal without sending sensitive data to third-party websites.

## Installation
Save the code as `peek.py` and run it with Python 3. No external libraries required.

## Features
- Decodes JWT Header and Payload.
- Does not perform network requests (100% offline).
- Supports piping from other commands.
- Pretty-prints JSON output.

## Usage

Pass the token as an argument:
python peek.py <your_jwt_token>

Or pipe a token from another command:
echo "your.jwt.token" | python peek.py