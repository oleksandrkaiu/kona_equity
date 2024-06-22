import requests
import json
import base64
import logging

# ***********************************************************************************
# @Function: Get Google Identity Token From Authorization Code
# @Returns: Process Result Or Identity Token
# -----------------------------------------------------------------------------------
def getIdentityTokenFromAuthzCode(authz_code, client_id, client_secret, redirect_url, grant_type="authorization_code", access_type="offline"):
    try:
        # ---------- send request to google idp to exchange authz code with identity token ---------- #
        res = requests.post("https://oauth2.googleapis.com/token",
                            json={
                                "code": authz_code,
                                "client_id": client_id,
                                "client_secret": client_secret,
                                "redirect_uri": redirect_url,
                                "grant_type": grant_type,
                                "access_type": access_type,
                            }, verify=False)
        if res.status_code != 200:
            return {'res': None, 'msg': "res.status_code %s" % (res.status_code)}
        res = res.json()
        if "id_token" not in res:
            logging.warning("Id token is not in response")
            return {'res': None, 'msg': "Id token is not in response"}

        # ---------- parse identity token ---------- #
        id_token = res["id_token"].split(".")[1]
        if id_token[-2:] != "==":
            id_token += "=="
        id_token = json.loads(base64.b64decode(id_token))
        return id_token

    except Exception as e:
        logging.warning(str(e))
        return {'res': None, 'msg': str(e)}