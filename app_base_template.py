import falcon, os
from falcon_cors import CORS
from resources import {{classes}}

CORZ = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
API = application = falcon.API(middleware=[CORZ.middleware])




