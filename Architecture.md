The project is reorganized into a modular, object-oriented structure designed for extensibility and maintainability. 

1. **Data Layer**: Utilizes Python Data Classes (`JWTPreview`) to enforce a structured schema for the decoded output, ensuring consistency across different consumption points.
2. **Logic Layer**: The `JWTDecoder` class encapsulates all transformation logic. It separates the concerns of Base64 padding correction, segment decoding, and overall token inspection. By making these methods static/class methods, the logic remains stateless and easily testable.
3. **Interface Layer**: The `CLIHandler` manages I/O operations. It abstracts the complexity of stream handling (stdin vs. argv), allowing the core decoding logic to remain agnostic of how the data was acquired.
4. **Error Handling**: Replaces generic catch-all exceptions with specific error types (JSONDecodeError, ValueError) and returns structured error messages rather than raw stack traces.
5. **Optimization**: Implements a more efficient padding calculation `(-len(segment) % 4)` and ensures PEP-8 compliance through strict type hinting and standardized naming conventions.