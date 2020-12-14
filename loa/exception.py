

class TeamConsistencyError(Exception):
    
    def __init__(self, team, message=None):
        self._team = team
        self._message = message
        super().__init__(self._message)
       
    @property
    def team(self):
        return self._team

    @property
    def message(self):
        return self._message


class ArrangeTimeoutError(Exception):
    def __init__(self, team, message=None):
        self._team = team
        self._message = message
        super().__init__(self._message)
       
    @property
    def team(self):
        return self._team

    @property
    def message(self):
        return self._message