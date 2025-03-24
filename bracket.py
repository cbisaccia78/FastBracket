import sys
import pickle
import json

from typing import List
from math import log2

from pydantic import ValidationError

class Team:
    def __init__(self, name: str, seed: int):
        if seed < 1:
            raise ValueError(f"Seed {seed} is not greater than 0.")
        
        self.name = name
        self.seed = seed

    def __eq__(self, other: "Team"):
        if type(other) != Team:
            raise TypeError("Tried to compare eq between Team and non-Team type")
        
        return (
            self.name == other.name and 
            self.seed == other.seed
        )

    def __hash__(self):
        return hash((self.name, self.seed))

    def __repr__(self):
        return f"{self.name}({self.seed})"


class Pairing:
    def __init__(self, team1: Team, team2: Team, round: int=1, pick: Team=None):
        if round < 1:
            raise ValueError(f"Round {round} must be greater than 0.")
        
        self.team1 = team1
        self.team2 = team2

        self.round = round

        self.pick = pick

        self.winner = None
        self.loser = None

        self.next = None
    
    def __eq__(self, other: "Pairing"):
        if type(other) != Pairing:
            raise TypeError("Tried to compare eq between Pairing and non-Pairing type")
        
        return (
            self.team1 == other.team1 and
            self.team2 == other.team2 and
            self.round == other.round and
            self.winner == other.winner and
            self.loser == other.loser
        )
    
    def __hash__(self):
        return hash((self.team1, self.team2, self.round))
    
    def __repr__(self):
        return f"{self.team1}\n{'-'*15}\n{' '*15}|\n{' '*15}|\n{' '*15}|\n{' '*15}|\n{self.team2}{' '*(15 - len(str(self.team2)))}|\n{'-'*15}"

    def calculate_score(self) -> float:
        if not self.finished or self.pick is None or self.pick != self.winner:
            return 0

        team1 = self.team1
        team2 = self.team2

        s1 = team1.seed
        s2 = team2.seed

        favorite, underdog = (team1, team2) if s1 < s2 else (team2, team1)

        if self.winner == favorite:
            return 2**(self.round - 1)
        else:
            return (underdog.seed / favorite.seed) * (2**(self.round - 1))
    
    @property
    def finished(self) -> bool:
        return not (self.winner is None or self.loser is None)

class Bracket:
    def __init__(self, owner: str, pairings: List[Pairing], total_teams: int, name="bracket"):
        if not log2(total_teams).is_integer():
            raise ValueError("Bracket size must be an exponent of 2")
        
        self._total_rounds = log2(total_teams) + 1
        self._validate_initial_pairings(pairings)

        self.owner: str = owner
        self.name: str = name
        # To-Do - currently cannot create an empty bracket because of hash collisions
        self.pairings = {hash(pairing): pairing for pairing in pairings} # hashmap from hashed pairing -> pairing so we can index into pairing through another pairing object
        self.winner: Team = None

    def update(self, pairing: Pairing) -> None:
        to_update = self.pairings.get(pairing, None)
        if to_update is None:
            # insert
            self.pairings[pairing] = pairing
        else:
            to_update.winner, to_update.loser = pairing.winner, pairing.loser
            
        # check if there's a winner
        if pairing.round == self._total_rounds:
            self.winner = pairing.winner

    def save(self, filepath="") -> None:
        if filepath == "":
            filepath = f"./{self.owner}-{self.name}.pkl"

        try:
            with open(filepath, "wb") as file:
                pickle.dump(self, file)
            print(f"Bracket pickled successfully to '{filepath}'")
        except Exception as e:
            print(f"Error during pickling: {e}")
    
    @property
    def current_score(self) -> int:
        return sum(pairing.calculate_score() for pairing in self.pairings.values())
    
    def _validate_initial_pairings(self, pairings: List[Pairing]) -> None:
        for pairing in pairings:
            if pairing.team1 is None or pairing.team2 is None or pairing.round > self._total_rounds:
                raise ValueError(f"Pairing {pairing} is invalid.")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        bracket_filepath = sys.argv[1]
        try:
            with open(bracket_filepath, "rb") as file:
                bracket = pickle.load(file)
            print(f"Bracket loaded successfully from '{bracket_filepath}'")
        except FileNotFoundError:
            print(f"Error: Bracket '{bracket_filepath}' not found.")
            exit(1)
        except Exception as e:
            print(f"Error during loading: {e}")
            exit(2)
    else:
        owner = input("Enter your name: ")
        bracket_name = input("Enter a name for your bracket: ")
        try:
            raw_pairings_list = json.loads(
                input("Enter a space separated list of json pairing objects of form [{team1: [name, seed], team2: [name, seed], round: round, [pick: [name, seed]], [winner: [name, seed]]}, ...]")
            )
            pairings_list = [Pairing(PairingBase(**raw_pairing)) for raw_pairing in raw_pairings_list]

        except json.JSONDecodeError:
            print("Invalid json structure for pairings list.")
            exit(3)
        except ValidationError as e:
            print(e.errors())
            exit(4)

    creighton = Team("creighton", 8)
    louisville = Team("louisville", 9)
    p = Pairing(creighton, louisville, 4)
    print(p)
    p.set_result(louisville)
    print(p.calculate_score())