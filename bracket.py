from typing import List

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
    def __init__(self, team1: Team, team2: Team, round: int=1):
        if round < 1:
            raise ValueError(f"Round {round} must be greater than 0.")
        
        self.team1 = team1
        self.team2 = team2

        self.round = round

        self.winner = None
        self.loser = None
    
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
        return hash((self.team1, self.team2))
    
    def __repr__(self):
        return f"{self.team1}\n{'-'*15}\n{' '*15}|\n{' '*15}|\n{' '*15}|\n{' '*15}|\n{self.team2}{' '*(15 - len(str(self.team2)))}|\n{'-'*15}"
    
    def set_result(self, winning_team: Team):
        if winning_team != self.team1 and winning_team != self.team2:
            raise ValueError(f"Winning team {winning_team} must be one of {self.team1} or {self.team2}")

        self.winner, self.loser = (self.team1, self.team2) if winning_team == self.team1 else (self.team2, self.team1)
    
    def calculate_score(self):
        if not self.finished:
            return -1

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
    def finished(self):
        return not (self.winner is None or self.loser is None)

class Bracket:
    def __init__(self, owner: str, pairings: List[List[Pairing]]):
        self.owner = owner
        
        self.pairings = {} # hashmap from hashed pairing -> pairing so we can index into pairing through another pairing object

    def update(self, pairings: List[Pairing], round: int):
        if round < 1 or round > len(self.pairings):
            raise ValueError(f"round {round} must be greater than 0 and less than the total number of rounds stored")
        potential_pairings = self.pairings[round]
        
        for 

    def calculate_score(self):
        score = 0
        for round_pairings in self.pairings:
            for pairing in round_pairings:
                if pairing.finished:
                    score += pairing.calculate_score()
        return score

creighton = Team("creighton", 8)
louisville = Team("louisville", 9)
p = Pairing(creighton, louisville, 4)
print(p)
p.set_result(louisville)
print(p.calculate_score())