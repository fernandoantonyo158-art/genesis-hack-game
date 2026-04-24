# { "Depends": "py-genlayer:latest" }
from genlayer import *

class GenesisHack(Contract):
    # Persistent storage for solved cases and detective status
    solved_detectives: Map[Address, bool]
    case_title: str

    def __init__(self):
        self.solved_detectives = Map[Address, bool]()
        self.case_title = "Case #01: The Genesis Hack"

    @gl.public.write
    def solve_case(self, player_address: Address, solution_attempt: str):
        """
        Intelligent verification of the case solution using GenLayer's AI Consensus.
        The AI evaluates if the provided solution matches the culprit's identity.
        """
        
        # Check if already solved to prevent double minting
        if self.solved_detectives.get(player_address, False):
            revert("Case already solved by this detective.")

        # 1. Non-deterministic block to use the GenLayer Intelligent Oracle (LLM)
        def verify_with_ai():
            prompt = (
                f"You are the Lead Investigator of the GenLayer Bureau. "
                f"The evidence for '{self.case_title}' suggests the culprit is a node operator "
                f"involved in a transaction at 03:14:07, known as 'The Architect'. "
                f"Is the name '{solution_attempt}' the correct identity of the culprit? "
                "Respond strictly with 'YES' or 'NO'."
            )
            return gl.nondet.llm.ask(prompt)

        # 2. Reach consensus via Equivalence Principle
        # GenLayer ensures all validators agree on the AI's verdict.
        verdict = gl.eq_principle.strict_eq(verify_with_ai)

        # 3. Finalize on-chain state
        if verdict.strip().upper() == "YES":
            self.solved_detectives[player_address] = True
            # In a full setup, this would trigger an event or interact with an NFT contract
            return "CASE SOLVED: Master Detective Status Granted."
        else:
            revert("INVALID SOLUTION: The evidence does not match your claim.")

    @gl.public.view
    def is_master_detective(self, detective: Address) -> bool:
        """Returns True if the address has successfully solved the case on-chain."""
        return self.solved_detectives.get(detective, False)
