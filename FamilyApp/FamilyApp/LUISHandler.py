from luis_sdk import luis_client
from luis_client import LUISClient


_LUIS_APP_ID = '1bb9ea2a-a69a-4ed1-923c-a8a13639bd80'
_LUIS_APP_SECRET = '43084cd2875341fea97ffd40fe1fb211'


LuisCl = LUISClient(_LUIS_APP_ID, _LUIS_APP_SECRET, True, True)


