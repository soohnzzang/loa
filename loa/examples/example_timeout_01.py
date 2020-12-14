from loa.unit import Unit
from loa.team import Team
from loa.team import TeamExaminer
from loa.simulator import EvasionSimulator
from loa.logging import use_logging, finish_logging
import time

class MyUnit1(Unit):
    
    HP = 10 # Hit Points (health points)    
    ATT = 6  # Attack
    ARM = 5  # Armor
    EVS = 0 # Evasion
        
    def __init__(self, team, name, pos):
        cls = __class__
        super().__init__(team,
                         name,
                         pos,
                         hp=cls.HP,
                         att=cls.ATT,
                         arm=cls.ARM,
                         evs=cls.EVS)

class MyUnit2(Unit):
    
    HP = 10  # Hit Points (health points)    
    ATT = 7  # Attack
    ARM = 4  # Armor
    EVS = 0  # Evasion
        
    def __init__(self, team, name, pos):
        cls = __class__
        super().__init__(team,
                         name,
                         pos,
                         hp=cls.HP,
                         att=cls.ATT,
                         arm=cls.ARM,
                         evs=cls.EVS)

class MyTeam1(Team):
    def initialize(self):
        for i in range(10):
            unit = MyUnit1(self, "A-Unit%02d"%(i+1), i)
            self.units.append(unit)
            
    def arrange(self, enemy: Team):        
        pass
    
class MyTeam2(Team):
    def initialize(self):
        for i in range(10):
            unit = MyUnit2(self, "B-Unit%02d"%(i+1), i)
            self.units.append(unit)
            
    def arrange(self, enemy: Team):
        time.sleep(0.05)

    
if __name__ == "__main__":
   
    use_logging("test",                
                stdout=False,
                fout=False,
                fpath="test.log",
                mode='w')
    
    simulator = EvasionSimulator()
    team1 = MyTeam1("Team#1")
    team2 = MyTeam2("Team#2")
    print(team1)
    print()
    print(team2)
    
    # Observe how the positions of team2 changes
    for i in range(5):
        team2.arrange(team1)
        print(team2)
    
    
    examiner = TeamExaminer()
    examiner.check(team1, "ROUND-02")
    examiner.check(team2, "ROUND-02")    

    n_team1, n_team2, n_draws = simulator.play(team1, team2, 20, 10)
    print("Number of Team1 wins:", n_team1)
    print("Number of Team2 wins:", n_team2)
    print("Number of draws:", n_draws)
    print()
    
    if n_team1 > n_team2:
        print("Team #1 wins!")
    elif n_team1 < n_team2:
        print("Team #2 wins!")        
    else:
        print("Two teams draw...")

    finish_logging()
        