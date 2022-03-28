from http.client import HTTPException
import requests
from dotenv import dotenv_values
from pydantic import BaseModel
from starlette import status

config_credentials = dotenv_values(".env")


class DataLookup(BaseModel):
    network: str
    type: str


def get_all_data_lookups(data_lookup):
    if config_credentials["PRODUCTION_STATUS"] == "FALSE":
        base_url = config_credentials["TEST_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}
    else:
        base_url = config_credentials["LIVE_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}

    datar = {
        "network": data_lookup.network,
        "type": data_lookup.type
    }

    try:
        r = requests.post(url=base_url + "/data/lookup", params=datar, headers=headers,)
        data = r.json()

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW.Authenticate": "Bearer"}
        )
    return data
