class GraphInfo(object):
    """description of class"""

    def __init__(self,expires_in,access_token,refresh_token,scope,id_token):
        self.expires_in = expires_in
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scope = scope
        self.id_token = id_token


class SpeakerInfo(object):
    """description of class"""

    def __init__(self,expires_in,access_token,refresh_token,profile_id):
        self.expires_in = expires_in
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.profile_id  =profile_id
