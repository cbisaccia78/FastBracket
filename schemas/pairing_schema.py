from pydantic import BaseModel, field_validator

class PairingBase(BaseModel):
    team1: str
    team2: str
    round: int

    pick: str | None = None
    winner: str | None = None

    @field_validator('team1')
    def validate_team1(cls, team):
        return PairingBase._validate_team(team)

    @field_validator('team2')
    def validate_team1(cls, team):
        return PairingBase._validate_team(team)

    @field_validator('pick')
    def validate_team1(cls, team):
        return PairingBase._validate_team(team)

    @field_validator('winner')
    def validate_team1(cls, team):
        return PairingBase._validate_team(team)

    def _validate_team(cls, team):
        if team is None:
            return None
        
        try:
            # Attempt to evaluate the string as a list
            parsed_list = eval(team)
            if not isinstance(parsed_list, list) or len(parsed_list) != 2:
                raise ValueError(f"{team} team string must represent a list with exactly two elements.")
            return team  # Return the original string if validation passes
        except (SyntaxError, TypeError):
            raise ValueError(f"{team} Invalid string format. Must be a string list representation of a team.")

