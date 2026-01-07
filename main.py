"""
Rock–Paper–Scissors–Plus AI Game Referee
CLI-based implementation aligned with Google ADK concepts
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List


def tool(func):
    return func

class Agent:
    def __init__(self, name, instructions, tools):
        self.name = name
        self.instructions = instructions
        self.tools = tools

VALID_MOVES = {"rock", "paper", "scissors", "bomb"}
MAX_ROUNDS = 3

@dataclass
class GameState:
    round: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    history: List[Dict] = field(default_factory=list)

    def is_game_over(self) -> bool:
        return self.round > MAX_ROUNDS

def parse_intent(user_input: str) -> Dict:
    text = user_input.lower().strip()

    if text in {"help", "rules"}:
        return {"intent": "help"}

    return {
        "intent": "play_move",
        "move": text
    }

@tool
def validate_move(move: str, player: str, state: Dict) -> Dict:
    if move not in VALID_MOVES:
        return {"valid": False, "error": "Invalid move"}

    if move == "bomb":
        if player == "user" and state["user_bomb_used"]:
            return {"valid": False, "error": "User bomb already used"}
        if player == "bot" and state["bot_bomb_used"]:
            return {"valid": False, "error": "Bot bomb already used"}

    return {"valid": True, "move": move}


@tool
def choose_bot_move(state: Dict) -> str:
    if not state["bot_bomb_used"] and state["user_score"] > state["bot_score"]:
        return "bomb"

    return random.choice(["rock", "paper", "scissors"])


@tool
def resolve_round(user_move: str, bot_move: str) -> str:
    if user_move == "bomb" and bot_move == "bomb":
        return "draw"

    if user_move == bot_move:
        return "draw"

    if user_move == "bomb":
        return "user"

    if bot_move == "bomb":
        return "bot"

    rules = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    return "user" if rules[user_move] == bot_move else "bot"


@tool
def update_game_state(
    state: Dict,
    user_move: str,
    bot_move: str,
    winner: str
) -> Dict:
    if user_move == "bomb":
        state["user_bomb_used"] = True

    if bot_move == "bomb":
        state["bot_bomb_used"] = True

    if winner == "user":
        state["user_score"] += 1
    elif winner == "bot":
        state["bot_score"] += 1

    state["history"].append({
        "round": state["round"],
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": winner
    })

    state["round"] += 1
    return state

agent = Agent(
    name="GameRefereeAgent",
    instructions="""
You are an AI referee for Rock–Paper–Scissors–Plus.
Use tools for validation, round resolution, and state updates.
Do not store state in the prompt.
End the game automatically after 3 rounds.
""",
    tools=[
        validate_move,
        choose_bot_move,
        resolve_round,
        update_game_state
    ]
)



def main():
    state = GameState().__dict__

    print("Referee Agent Loaded:", agent.name)

    print("""
Rock–Paper–Scissors–Plus
Rules:
- Best of 3 rounds
- Moves: rock, paper, scissors, bomb
- Bomb can be used once per player
- Invalid input wastes the round
""")

    while not GameState(**state).is_game_over():
        print(f"\n--- Round {state['round']} ---")
        user_input = input("Your move: ")

        intent = parse_intent(user_input)

        if intent["intent"] == "help":
            print("Valid moves: rock, paper, scissors, bomb")
            continue

        validation = validate_move(intent["move"], "user", state)

        if not validation["valid"]:
            print("Invalid input. This round is counted as a loss.")
            state["round"] += 1
            continue

        user_move = validation["move"]
        bot_move = choose_bot_move(state)

        winner = resolve_round(user_move, bot_move)
        state = update_game_state(state, user_move, bot_move, winner)

        print(f"User move: {user_move}")
        print(f"Bot move: {bot_move}")

        if winner == "draw":
            print("Round result: DRAW")
        else:
            print(f"Round winner: {winner.upper()}")

    print("\nGAME OVER")
    print(f"Final Score -> User: {state['user_score']} | Bot: {state['bot_score']}")

    if state["user_score"] > state["bot_score"]:
        print("RESULT: USER WINS")
    elif state["user_score"] < state["bot_score"]:
        print("RESULT: BOT WINS")
    else:
        print("RESULT: DRAW")


if __name__ == "__main__":
    main()
