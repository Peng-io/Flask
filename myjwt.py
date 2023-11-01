import time

import jwt

myKey = "ifjhasiufhsaiufnASIFUHasui"

header = {"typ": "JWT", "alg": "HS256"}


def my_payload(user: str) -> dict:
    return {
        "iat": time.time(),
        "ext": int(time.time()) + 60 * 60 * 20 * 30,
        "user": user,
    }


def set_token(user: str) -> str:
    return jwt.encode(
        payload=my_payload(user), key=myKey, algorithm="HS256", headers=header
    )


def get_token(key: str) -> bool:
    try:
        data = jwt.decode(key, myKey, algorithms="HS256")
    except:
        return False
    else:
        if data.pop("ext") < time.time():
            return False
        else:
            return True
