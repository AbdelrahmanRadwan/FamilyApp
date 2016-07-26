class GraphInfo(object):
    """description of class"""

    def __init__(self,auth_code=None,expires_in=None,access_token=None,refresh_token=None,scope=None,id_token=None, user_info_json=None):
        self.auth_code = auth_code
        self.expires_in = expires_in
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scope = scope
        self.id_token = id_token
        self.user_info_json = user_info_json

    def getISS(self):
        return self.user_info_json["iss"]

    def getTID(self):
        return self.user_info_json["tid"]

    def getSUB(self):
        return self.user_info_json["sub"]

class SpeakerInfo(object):
    """description of class"""

    def __init__(self,profile_id):
        self.profile_id  =profile_id
