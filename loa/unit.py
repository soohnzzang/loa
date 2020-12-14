from __future__ import annotations

from loa.logging import write_log
from loa import utils

class Unit:    
    def __init__(self,
                 team = None,
                 name: str = "",
                 pos: int = 0,
                 hp: float = 0,
                 att: float = 0,
                 arm: float = 0,
                 evs: float = 0):
        
        self.team = team  # Team that this unit belongs to.
        self.name = name  # Name of this unit.
        
        self.pos = pos    # Position (index) in the team.
        
        self.hp = hp      # Hit Points (HP)
        self.att = att    # Attack Damage (ATT)
        self.arm = arm    # Armor (ARM)
        self.evs = evs    # Evasion (EVS)
        
    def __str__(self):
        fstr = "%s(NAME:%s,POS:%d,HP:%.2f,ATT:%.2f,ARM:%.2f,EVS:%.2f)"
        return fstr%(self.__class__.__name__,
                     self.name,
                     self.pos,
                     self.hp,
                     self.att,
                     self.arm,
                     self.evs)

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if not other:
            return False
            
        attr1 = (self.name,
                 self.hp,
                 self.att,
                 self.arm,
                 self.evs)
        attr2 = (other.name,
                 other.hp,
                 other.att,
                 other.arm,
                 other.evs)
        
        return attr1 == attr2
        
    def __ne__(self, other):        
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(str(self))
    
    # Properties
    @property
    def team(self):
        return self._team
    
    @team.setter
    def team(self, team):
        from loa import Team
        utils.check_type("team", team, Team)            
        self._team = team
    
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, val):
        utils.check_type("name", val, str)
        self._name = val
        
    @property
    def pos(self):
        return self._pos
        
    @pos.setter
    def pos(self, val: int):
        utils.check_nonnegative_int("pos", val)
        self._pos = val        
    
    @property
    def hp(self):
        return self._hp
        
    @hp.setter
    def hp(self, val: float):
        utils.check_nonnegative_float("hp", val)
        self._hp = val
    
    @property
    def att(self):
        return self._att
    
    @att.setter
    def att(self, val: float):
        utils.check_nonnegative_float("att", val)
        self._att = val

    @property
    def arm(self):
        return self._arm
    
    @arm.setter
    def arm(self, val: float):
        utils.check_nonnegative_float("arm", val)
        self._arm = val   

    @property
    def evs(self):
        return self._evs
    
    @evs.setter
    def evs(self, val: float):
        utils.check_nonnegative_float("evs", val)
        self._evs = val

    @property
    def magics(self):
        return self._magics
    
    # Methods
    def attack(self, target: Unit):        
        utils.check_type("target", target, Unit)
        write_log(
            "Before attack, %s.%s.hp=%.2f, %s.%s.hp=%.2f"%
            (
                self.team.name,
                self.name,
                self.hp,
                target.team.name,
                target.name,
                target.hp
            )
        )
        
        target.hp = max(0, target.hp - max(1, self.att - target.arm))
        self.hp = max(0, self.hp - max(1, 0.5*target.att - self.arm))

        write_log("%s.%s attacks %s.%s"%(self.team.name,
                                         self.name,
                                         target.team.name,
                                         target.name))
        write_log(
            "After attack, %s.%s.hp=%.2f, %s.%s.hp=%.2f"%
            (
                self.team.name,
                self.name,
                self.hp,
                target.team.name,
                target.name,
                target.hp
            )
        )
         
    def update(self, obj: Unit):
        utils.check_type("obj", obj, Unit)        
        self.name = obj.name
        self.hp = obj.hp
        self.att = obj.att
        self.arm = obj.arm
        self.evs = obj.evs
