import json
import base64
import sys

class TournamentCodeException(Exception):
    pass

class lolTournamentCode(object):
    def __init__(self,tournament_name,team1,team2,password,report_url,extra_data,team_size):
        self.name = tournament_name+'_'+team1+'vs'+team2
        self.password = password
        self.report_url = 'lol-reports.s3-website-us-west-2.amazonaws.com'
        self.extra_data = extra_data
        self.team_size = team_size # only supports ints from 1 to 5
        self.map = {"The Crystal Scar":8,
                    "Twisted Treeline":10,
                    "Summoner's Rift":11,
                    "Howling Abyss":12}
        self.pick = {"BLIND PICK":1,
                    "DRAFT MODE":2,
                    "ALL RANDOM":4,
                    "TOURNAMENT DRAFT":6}
        self.spec = {'NONE':'NONE',
                    'ALL':'ALL',
                    'LOBBY':'LOBBYONLY'}

    def get_map(self):
        return self.map

    def get_pick(self):
        return self.pick

    def get_spec(self):
        return self.spec

    def generate(self,Map,pick,spec):
        try:
            self.mapID = self.map[Map]
        except:
            return 'Map type unavailable'
        try:
            self.pickID = self.pick[pick]
        except:
            return 'Pick type unavailable'
        try:
            self.specID = self.spec[spec]
        except:
            return 'Spectator type unavailable'
        if self.mapID == 10 and self.team_size > 3:
            raise TournamentCodeException('Maximum team size in twisted treeline is 3')
        otherData = self.serialize()
        return self.build(self.mapID,self.pickID,self.team_size,self.specID,otherData)

    def build(self,mapId,pick,team_size,specID,otherData):
        return ("pvpnet://lol/customgame/joinorcreate/"
                "map"+str(mapId)+"/pick"+str(pick)+"/team"+str(team_size)+
                "/spec"+str(specID)+"/"+otherData)

    def serialize(self):
        return base64.b64encode(json.dumps({
            "name": self.name,
            "password": self.password,
            "report": self.report_url,
            "extra": json.dumps(self.extra_data),
        }))

if __name__ == '__main__':
    test = lolTournamentCode('cteemo','doubi','shadixx','54.149.235.253/match_report/lol','',1,3)
    print test.generate("Twisted Treeline","TOURNAMENT DRAFT","ALL")