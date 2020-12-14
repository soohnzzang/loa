import copy
import random

from loa import utils
from loa.unit import Unit
from loa.team import Team
from loa.logging import write_log

from loa.team import TeamExaminer
from loa.judge import Judge, MaxSurvivalJudge


class Simulator:    

    def __init__(self, league_round=None):
        
        if not league_round:
            league_round = utils.get_current_round()
        
        self._league_round = league_round
        self._examiner = TeamExaminer()
             
    def play(self,
             team1: Team,
             team2: Team,             
             num_turns: int = 10,
             num_repeats: int =10,
             judge: Judge = None):
        
        utils.check_type("team1", team1, Team)
        utils.check_type("team2", team2, Team)
        utils.check_type("judge", judge, Judge, allow_none=True)
        
        if not judge:
            judge = MaxSurvivalJudge()

        if len(team1) != len(team2):
            err_msg = "The sizes of team1 and team2 dost not match!"
            write_log(err_msg)
            raise ValueError(err_msg)
        
        num_wins_team1 = 0
        num_wins_team2 = 0
        num_draws = 0
        
        for i in range(num_repeats):            
            team1_cpy = copy.deepcopy(team1)
            team2_cpy = copy.deepcopy(team2)
            if i % 2 == 0:
                offense, defense = team1_cpy, team2_cpy
            else:
                offense, defense = team2_cpy, team1_cpy
                
            judge.initialize()
            for t in range(num_turns):
                write_log("[%s vs %s - Repeat #%d Turn #%d]"%(team1.name,
                                                              team2.name,
                                                              i+1,
                                                              t+1))
                
                self._examiner.check_play(offense,
                                          defense,
                                          self._league_round)
                
                # Arrange
                defense_cpy = copy.deepcopy(defense)
                offense.arrange(defense_cpy)
                
                # Attack
                self._apply_attack(offense, defense)
            
                self._clear_dead_units(offense)
                self._clear_dead_units(defense)
                write_log("#Units in %s=%d, #Units in %s=%d"%(team1.name,
                                                              len(team1_cpy),
                                                              team2.name,
                                                              len(team2_cpy)))
                
                judge.update(t, team1_cpy, team2_cpy)
                if len(offense) == 0 or len(defense) == 0:
                    break                                        
                
                offense, defense = defense, offense                
            # end of for
            
            winner = judge.decide(team1_cpy, team2_cpy)
            if winner == team1.name:
                num_wins_team1 += 1
            elif winner == team2_cpy.name:
                num_wins_team2 += 1
            else:  # Draw
                num_draws += 1

        # end of for
        
        return num_wins_team1, num_wins_team2, num_draws
     
      
    def _apply_attack(self, offense: Team, defense: Team):
        raise NotImplementedError()
        
    def _clear_dead_units(self, team: Team):
        for i, unit in enumerate(team):
            if not unit:
                continue
            
            if unit.hp <= 0:
                team[i] = None
                write_log("%s.%s has been dead..."%(unit.team.name, unit.name))
# end of class            


class BasicSimulator(Simulator):
    
    def _apply_attack(self, offense: Team, defense: Team):
        for i, unit in enumerate(offense):            
            target = defense[i]
            if unit and target:
                unit_cpy = copy.deepcopy(unit)
                target_cpy = copy.deepcopy(defense[i])
                unit.attack(target)

                # Check consistency                
                utils.attack(unit_cpy, target_cpy, Unit)
                if unit_cpy != unit:
                    err_msg = "%s.attack() performs "\
                              "illegal behaviors!"%(unit.__class__)
                    write_log(err_msg)
                    raise RuntimeError(err_msg)
# end of class               
                    
class EvasionSimulator(Simulator):
    
    def _apply_attack(self, offense: Team, defense: Team):
        for i, unit in enumerate(offense):            
            target = defense[i]
            if unit and target:
                if self._try_evasion(target):
                    continue
                
                unit_cpy = copy.deepcopy(unit)
                target_cpy = copy.deepcopy(defense[i])
                unit.attack(target)

                # Check consistency                
                utils.attack(unit_cpy, target_cpy, Unit)
                if unit_cpy != unit:
                    err_msg = "%s.attack() performs "\
                              "illegal behaviors!"%(unit.__class__)
                    write_log(err_msg)
                    raise RuntimeError(err_msg)
    
    def _try_evasion(self, target):
        evsr = target.evs / 100.  # Evasion Rate (EVSR)
        rn = random.uniform(0, 1)
        if rn  <= evsr:
            write_log("%s evades with %.4f! (RN: %.4f)."%(target.name, evsr, rn))
            return True
            
        return False       