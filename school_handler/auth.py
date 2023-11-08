import re
import uuid

import requests

login_action_pattern = re.compile(r'(?P<LoginActionURL>https://.+?)"')
oauth_code_pattern = re.compile(r'code=(?P<OAuthCode>[^&$]+)[&$]?')


def get_auth_info(login, password):
    state = str(uuid.uuid4())
    nonce = str(uuid.uuid4())

    session = requests.Session()

    response = requests.get(
        f"https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/auth?client_id=school21&redirect_uri=https%3A%2F%2Fedu.21-school.ru%2F&state={state}&response_mode=fragment&response_type=code&scope=openid&nonce={nonce}",
        timeout=5)

    if response.status_code != 200:
        return None

    session.cookies.update(response.cookies)

    new_url = login_action_pattern.search(response.text).group("LoginActionURL").replace("amp;", "")

    response = session.post(new_url, data={"username": login, "password": password},
                            allow_redirects=False)

    if response.status_code != 302:
        return None

    session.cookies.update(response.cookies)

    location = response.headers.get("location")

    response = session.post(location, allow_redirects=False)

    if response.status_code != 302:
        return None

    location = response.headers.get("location")

    auth_code = oauth_code_pattern.search(location).group("OAuthCode")
    session.cookies.update(response.cookies)

    response = session.post("https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token",
                            data={
                                "code": auth_code,
                                "grant_type": "authorization_code",
                                "client_id": "school21",
                                "redirect_uri": "https://edu.21-school.ru/"
                            })

    if response.status_code != 200:
        return None
    print(response.json()["access_token"])
    return response
