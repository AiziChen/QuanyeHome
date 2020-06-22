import requests
import json
import time
import urllib.parse

BASE_URL = "http://oa.xinlvyao.com:89"


def create_signin(sessionkey, data, cookies):
    resp = requests.post(
        BASE_URL + "/client.do?method=postjson&module=17&scope=16" +
        "&operation=create&sessionkey=" + sessionkey, params=data, cookies=cookies)
    c = resp.content.decode("utf-8")
    print(c)
    if c.find("error") < 0:
        return True
    else:
        return False


def login(user, password):
    '''
    login operation: return sessionkey
    '''
    resp = requests.post(
        BASE_URL + "/client.do",
        params="method=login&loginid=" + user +
        "&password=" + password +
        "&isneedmoulds=1&client=1&clientver=6.6.0.1&udid=867401041480114&token=&clientos=PKQ1.190202.001&clientosver=9&clienttype=android&language=zh&country=CN&authcode=&dynapass=&tokenpass=&relogin=0&clientuserid=&tokenFromThird=&signatureValue=&signAlg=&randomNumber=&cert="
    )
    if (resp.ok):
        h = resp.headers['Set-Cookie']
        hs = h.split(",")
        for v in hs:
            if v.find("JSESSIONID") > 0:
                key = v[v.index("=") + 1: v.index(";")]
                return (key, resp.cookies)
    return (False, "error")


def do_signin(user, password, data):
    key, cookies = login(user, password)
    if key == False:
        return False
    else:
        return create_signin(key, data, cookies)


# rs = do_signin("chenqy", "", "latitudeLongitude=22.571694999999995,113.853659" +
#                "&address=广东省深圳市宝安区金海路3008靠近海港小学" +
#                "&remark=&attachmentIds=")
# print(rs)
