# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class GenesisHack(gl.Contract):
    # Persistent storage for solved cases and detective status
    solved_detectives: TreeMap[str, bool]
    case_title: str

    def __init__(self):
        # Initialize the TreeMap and the case title
        self.solved_detectives = TreeMap[str, bool]()
        self.case_title = "Case #01: The Genesis Hack"

    @gl.public.write
    def solve_case(self, solution_attempt: str) -> str:
        # 1. Automatically get the player's wallet address
        player_address = gl.msg.sender

        # 2. Security Check: Has this detective already solved the case?
        if self.solved_detectives.get(player_address) is not None:
            raise Exception("Case already solved by this detective.")

        # 3. AI Investigation Logic
        def verify_with_ai() -> str:
            prompt = (
                f"You are the Lead Investigator of the GenLayer Bureau. "
                f"The evidence for '{self.case_title}' suggests the culprit is a node operator "
                f"involved in a transaction at 03:14:07, known as 'The Architect'. "
                f"Is the name '{solution_attempt}' the correct identity of the culprit? "
                "Respond strictly with 'YES' or 'NO'."
            )
            return gl.nondet.llm.ask(prompt)

        # 4. Consensus on the AI's verdict
        verdict = gl.eq_principle.strict_eq(verify_with_ai)

        # 5. Final Result Processing
        if verdict.strip().upper() == "YES":
            # Save the success state on-chain
            self.solved_detectives[player_address] = True
            
            # Emit an event for the frontend to react (animations, sounds, etc.)
            gl.emit_event("CaseSolved", {"detective": player_address, "suspect": solution_attempt})
            
            return "CASE SOLVED: Master Detective Status Granted."
        else:
            raise Exception("INVALID SOLUTION: The evidence does not match your claim.")

    @gl.public.view
    def is_master_detective(self, detective: str) -> bool:
        # Check if a specific address has solved the case
        return self.solved_detectives.get(detective.lower()) is not None
