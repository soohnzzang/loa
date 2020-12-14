
from loa.team import Team

class JudgeFactory:
   
    @staticmethod
    def create(name):
        pass
        # if league_round == "round-1":
        #     pass
        # elif league_roud == "round-2":
        #     pass
        
        

class Judge:
    def __init__(self):        
        self.initialize()
        
    def initialize(self):
        pass

    def update(self,
               turn: int,
               team1: Team,
               team2: Team):
        """update() is called every turn
        """
        pass
        
    def decide(self, team1: Team, team2: Team):
        raise NotImplementedError()
        
class MaxSurvivalJudge(Judge):

    def decide(self, team1: Team, team2: Team):
        n_team1, n_team2 = len(team1), len(team2)
        
        if n_team1 > n_team2:
            return team1.name       
        elif n_team1 < n_team2:
            return team2.name
        else:
            return None    
    
class EachTurnMaxSurvivalJudge(Judge):
        
    def initialize(self):
        self._n_wins_team1 = 0
        self._n_wins_team2 = 0
        self._n_draws = 0
        
    def update(self,
               turn: int,
               team1: Team,
               team2: Team):

        if turn < 2:
            return        
        elif turn % 2 == 0:
            n_team1, n_team2 = len(team1), len(team2)

            if n_team1 > n_team2:
                self._n_wins_team1 += 1
            elif n_team1 < n_team2:
                self._n_wins_team2 += 1
            else:
                self._n_draws += 1
    
    def decide(self, team1: Team, team2: Team):
        if self._n_wins_team1 > self._n_wins_team2:
            return team1.name          
        elif self._n_wins_team1 < self._n_wins_team2:
            return team2.name
        else:
            if self._n_wins_team1 == self._n_wins_team2 == 0:
                n_team1, n_team2 = len(team1), len(team2)        
                if n_team1 > n_team2:
                    return team1.name       
                elif n_team1 < n_team2:
                    return team2.name
                else:
                    return None    
            return None            
    