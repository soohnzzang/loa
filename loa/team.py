from __future__ import annotations
from typing import List
from os.path import join as pjoin
import copy
import time

import yaml

from loa import utils
from loa.unit import Unit
from loa.logging import write_log
from loa.exception import TeamConsistencyError
from loa.exception import ArrangeTimeoutError


class Team:
    def __init__(self,
                 name: str,
                 units: List[Unit] = None):
        
        utils.check_type("name", name, str)
        self._name = name
        
        if units:
            utils.check_type("units", units, list)
            if len(units) != 0:
                utils.check_type("units[0]", units[0], Unit)
        else:
            units = []
            
        self._units = units
        self.initialize()
        
        
        
    def __str__(self):
        str_units = "\n".join([str(elem) for elem in self._units])
        fstr = "[%s(%s)]\n%s"
        return fstr%(self.__class__.__name__,
                     self.name,
                     str_units)
    
    
    def __repr__(self):
        return str(self)
    
    def __len__(self):
        return len(list(filter(lambda x: x, self._units)))
    
    def __getitem__(self, i):
        return self._units[i]
    
    def __setitem__(self, i, obj):
        self._units[i] = obj
        
    def __eq__(self, other: Team):        
        set_team1 = set(self.units)
        set_team2 = set(self.units)
        
        return set_team1 == set_team2
            

    def __ne__(self, other: Team):        
        return not self.__eq__(other)
        
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        utils.check_type("name", val, str)
        self._name = val
        
    @property
    def units(self) -> List[Unit]:
        return self._units

    @property
    def num_positions(self):
        return len(self._units)

    @property
    def num_units(self):
        return len(self)

            
    def initialize(self):
        """Create unit instances and arrange them.        
           
           for i in range(10):
               self.units.append(self, "MyUnit", i)
        """
        pass

    def arrange(self, enemy: Team):
        raise NotImplementedError()
        # Implement your arrangement strategy at each turn.
              
        
class TeamExaminer:
    
    def __init__(self, fname_constraints=None):
                        
        if not fname_constraints:
            fname_constraints = "constraints.yml"
            
        self._constraints = utils.load_constraint(fname_constraints)
        

    
    def check(self, team: Team, league_round: str = None):
        self._check_types(team)
        self._check_name(team)
        self._check_attributes(team)
        self._check_positions(team)
        self._check_constraints(team, league_round)
        self._check_arrange(team, copy.deepcopy(team), league_round)
    
    def check_play(self,
                   offense: Team,
                   defense: Team,
                   league_round: str = None):

        self._check_types(offense)
        self._check_types(defense)
        
        self._check_name(offense)
        self._check_name(defense)
        
        self._check_attributes(offense)
        self._check_attributes(defense)

        self._check_positions(offense)        
        self._check_positions(defense)

        self._check_arrange(offense, defense, league_round)
        
    def _check_unit_type(self, unit: Unit):
        if not isinstance(unit, Unit):
            err_msg = "An element of Team should be Unit type, " \
                      "not %s!"%(type(unit))
            raise TypeError(err_msg)
            
                
    def _check_unit_attribute(self, unit: Unit, attr: str):        
        if not hasattr(unit, attr):
            err_msg = "[%s] Unit should have attribute: %s!" \
                      %(type(unit), attr)
            raise AttributeError(err_msg)
            
    def _check_team_attribute(self, team: Team, attr: str):        
        if not hasattr(team, attr):
            err_msg = "[%s] Unit should have attribute: %s!" \
                      %(type(team), attr)
            raise AttributeError(err_msg)
            
    def _check_types(self, team: Team):
        utils.check_type("team", team, Team)        
        for unit in team:
            if unit is None:
                continue

            self._check_unit_type(unit)
        # end of for
    
    def _check_name(self, team: Team):
        if team.name.isspace() or len(team.name.split()) == 0:
            err_msg = "Team name cannot be whitespace!"
            write_log(err_msg)
            raise ValueError(err_msg)
    
    def _check_attributes(self, team: Team):
        utils.check_type("team", team, Team)
        
        self._check_team_attribute(team, "name")
        self._check_team_attribute(team, "units")
        self._check_team_attribute(team, "num_units")
        self._check_team_attribute(team, "num_positions")
        
        
        for unit in team:
            if unit is None:
                continue

            self._check_unit_type(unit)            
            self._check_unit_attribute(unit, "HP")
            self._check_unit_attribute(unit, "ATT")
            self._check_unit_attribute(unit, "ARM")
            self._check_unit_attribute(unit, "EVS")
            
            self._check_unit_attribute(unit, "name")
            self._check_unit_attribute(unit, "pos")
            self._check_unit_attribute(unit, "hp")
            self._check_unit_attribute(unit, "att")
            self._check_unit_attribute(unit, "arm")
            self._check_unit_attribute(unit, "evs")
        # end of for
        
                
    def _check_positions(self, team: Team):
        for i, unit in enumerate(team):
            if unit and unit.pos != i:
                err_msg = "[%s] The position of the unit " \
                          "is different from the real position %d, not %d."
                raise ValueError(err_msg%(team.name, i, unit.pos))
                
                
        
    def _check_unit_uniqueness(self, team: Team):
                
        set_ids = set([id(unit) for unit in team])
                
        if len(set_ids) != len(team):
            err_msg = "[%s] Each unit should be unique! " \
                      "%s includes redundant unit instances."%(team.name,
                                                               team.name)
            write_log(err_msg)
            raise RuntimeError(err_msg)
        
    def _check_constraints(self, team: Team, league_round=None):
        constraints = self._constraints
        
        if not league_round:
            league_round = "ROUND-01"
            
        league_round = league_round.upper()
        if league_round == "ROUND-01":
            CONS_TEAM = constraints[league_round]['TEAM']
            CONS_NUM_UNITS = CONS_TEAM['NUM_UNITS']
            CONS_UNIT_MAX_EVS = CONS_TEAM['UNIT_MAX_EVS']
            CONS_SUM_HP_ATT_ARM = CONS_TEAM['SUM_HP_ATT_ARM']
            CONS_SUM_UNIT_EVS_DIV_ARM = CONS_TEAM['SUM_UNIT_EVS_DIV_ARM']
            
            
            if len(team) != CONS_NUM_UNITS:
                err_msg = "[%s] The number of units should be" \
                          " %d, not %d"%(team.name, CONS_NUM_UNITS, len(team))
                write_log(err_msg)
                raise ValueError(err_msg)
            
            sum_hp = 0
            sum_att = 0
            sum_arm = 0
            sum_unit_evs_div_arm = 0
            for unit in team:
                if unit.evs > CONS_UNIT_MAX_EVS:
                    err_msg = "[%s] The evs of each unit should be " \
                              "less than or equal to %.2f, not %.2f!"% \
                              (
                                  unit.name,
                                  CONS_UNIT_MAX_EVS,
                                  unit.evs
                              )
                    write_log(err_msg)
                    raise ValueError(err_msg)
                # end of if
                sum_hp += unit.hp
                sum_att += unit.att
                sum_arm += unit.arm
                sum_unit_evs_div_arm += (float(unit.evs) / float(unit.arm))
            # end of for

            sum_hp_att_arm = sum_hp + sum_att + sum_arm
            if round(sum_hp_att_arm, 4)  > CONS_SUM_HP_ATT_ARM:
                err_msg = "[%s] The summation of HP, ATT, and ARM " \
                          "of all units in a team should be less than " \
                          "or equal to %.2f, not %.2f!"% \
                          (
                              team.name,
                              CONS_SUM_HP_ATT_ARM,
                              sum_hp_att_arm
                          )
                write_log(err_msg)
                raise ValueError(err_msg)
                
            if round(sum_unit_evs_div_arm, 4)  > CONS_SUM_UNIT_EVS_DIV_ARM:
                err_msg = "[%s] The summation of EVS/ARM of all units " \
                          "in a team should be less than or " \
                          "equal to %.2f, not %.2f!"% \
                          (
                              team.name,
                              CONS_SUM_UNIT_EVS_DIV_ARM,
                              sum_unit_evs_div_arm
                          )
                write_log(err_msg)
                raise ValueError(err_msg)
                
        elif league_round == "ROUND-02":
            CONS_TEAM = constraints[league_round]['TEAM']
            CONS_NUM_UNITS = CONS_TEAM['NUM_UNITS']
            CONS_UNIT_MAX_ATT = CONS_TEAM['UNIT_MAX_ATT']
            CONS_UNIT_MIN_HP = CONS_TEAM['UNIT_MIN_HP']
            CONS_UNIT_MAX_EVS = CONS_TEAM['UNIT_MAX_EVS']
            CONS_UNIT_SUM_HP_ATT_1d5ARM = CONS_TEAM['UNIT_SUM_HP_ATT_1d5ARM']
            
            
            if len(team) != CONS_NUM_UNITS:
                err_msg = "[%s] The number of units should be" \
                          " %d, not %d"%(team.name, CONS_NUM_UNITS, len(team))
                write_log(err_msg)
                raise ValueError(err_msg)
            
            
            for unit in team:
                if unit.ATT > CONS_UNIT_MAX_ATT:
                    err_msg = "[%s] The ATT of each unit should be " \
                              "less than or equal to %.2f, not %f!"% \
                              (
                                  unit.name,
                                  CONS_UNIT_MAX_ATT,
                                  unit.ATT
                              )
                    write_log(err_msg)
                    raise ValueError(err_msg)
                # end of if
                
                if unit.HP < CONS_UNIT_MIN_HP:
                    err_msg = "[%s] The HP of each unit should be " \
                              "greater than or equal to %.2f, not %f!"% \
                              (
                                  unit.name,
                                  CONS_UNIT_MIN_HP,
                                  unit.HP
                              )
                    write_log(err_msg)
                    raise ValueError(err_msg)
                # end of if
                
                
                if unit.evs > 0:
                    err_msg = "[%s] The evs of each unit should be zero, " \
                              "not %.2f!"%(unit.name, unit.evs)
                    write_log(err_msg)
                    raise ValueError(err_msg)
                # end of if
                sum_unit_hp_att_1d5arm = (unit.HP + unit.ATT + 1.5*unit.ARM)
                if sum_unit_hp_att_1d5arm > CONS_UNIT_SUM_HP_ATT_1d5ARM:
                    err_msg = "[%s] The summation of HP, ATT and 1.5*ARM of " \
                              "each unit should be less than or " \
                              "equal to %.2f, not %f!"% \
                              (
                                  team.name,
                                  CONS_UNIT_SUM_HP_ATT_1d5ARM,
                                  sum_unit_hp_att_1d5arm
                              )
                    write_log(err_msg)
                    raise ValueError(err_msg)
                # end of if
                
            # end of for
            
        else:
            err_msg = "league_round=%s is not defined!"%(league_round)
            write_log(err_msg)
            raise ValueError(err_msg)
                
    def _get_time_limit(self, league_round=None):
        if not league_round:
            league_round = "ROUND-01"
                    
        league_round = league_round.upper()
        if league_round in ("ROUND-01", "ROUND-02"):
            CONS_TEAM = self._constraints[league_round]['TEAM']
            if 'ARRANGE_TIME_LIMIT' in CONS_TEAM:
                return CONS_TEAM['ARRANGE_TIME_LIMIT']
        # end of if
        return 10000
            
    def _check_arrange(self,
                       offense: Team,
                       defense: Team,
                       league_round=None):
        
        offense_cpy = copy.deepcopy(offense)
        defense_cpy = copy.deepcopy(defense)
        
        t_beg = time.perf_counter()
        offense_cpy.arrange(defense_cpy)
        t_end = time.perf_counter()
        t_elapsed = t_end - t_beg
        t_limit = self._get_time_limit(league_round)
        if t_elapsed > t_limit:
            err_msg = "[%s] The duration of arrangement " \
                      "should be less than or " \
                      "equal to %f, not %f!"% \
                      (
                          offense.name,
                          t_limit,
                          t_elapsed
                      )
            write_log(err_msg)
            raise ArrangeTimeoutError(offense, err_msg)
        
        self._check_consistency(offense,
                                offense_cpy,
                                "arrangement")
    
    
    def _check_consistency(self,
                           origin: Team,
                           copied: Team,
                           situation: str):
          
        if len(origin) != len(copied):
            err_msg = "[%s] The size of the team " \
                      "has been changed in %s!"%(origin.name, situation)
            write_log(err_msg)
            raise TeamConsistencyError(origin, err_msg)
            
    
        if origin != copied:
            err_msg = "[%s] The units has been changed " \
                      "during %s!"%(origin.name, situation)
            write_log(err_msg)
            raise TeamConsistencyError(origin, err_msg) 
                
        
    
