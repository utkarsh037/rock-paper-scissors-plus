## Rock–Paper–Scissors–Plus AI Game Referee

### Overview
This project implements a minimal AI Game Referee for a Rock–Paper–Scissors–Plus game.
The referee enforces rules, tracks state across turns, and provides clear round-by-round
feedback using a simple CLI-based conversational loop.

### State Model
Game state is stored in a dedicated `GameState` dataclass that tracks:
- Current round number (max 3)
- User and bot scores
- Bomb usage for each player
- Round history

This ensures state persistence across turns and avoids storing logic in prompts.

### Agent & Tool Design
The solution follows a Google ADK-style architecture:
- An Agent abstraction defines the referee’s responsibilities
- Explicit tools are used for:
  - Move validation
  - Round resolution
  - Game state updates

All state mutations occur through tools to maintain a clean separation of concerns.

### Tradeoffs
- The bot strategy is intentionally simple to keep logic transparent and easy to reason about
- Google ADK primitives are mocked locally since the SDK is not publicly installable
- The interface is CLI-based to prioritize correctness over UI polish

### Future Improvements
With more time, this could be extended with:
- Smarter bot strategies
- Structured JSON outputs
- Multi-agent separation (intent parsing vs referee logic)
