import time

import jwt

myKey = "ifjhasiufhsaiufnASIFUHasui"

header = {
    "typ": "JWT",
    "alg": "HS256"
}


def MyPayLoad(user: str) -> dict:
    return {
        "iat": time.time(),
        "ext": int(time.time()) + 60 * 60 * 20 * 30,
        "user": user
    }


def setToKen(user: str) -> str:
    return jwt.encode(payload=MyPayLoad(user), key=myKey, algorithm="HS256", headers=header)


def getToKen(key: str) -> bool:
    try:
        data = jwt.decode(key, myKey, algorithms="HS256")
    except Exception as e:
        print(e)
        return False
    else:
        if data.pop("ext") < time.time():
            return False
        else:
            return True
