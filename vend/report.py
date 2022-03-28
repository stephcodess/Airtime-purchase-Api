from http.client import HTTPException
import requests
from dotenv import dotenv_values
from pydantic import BaseModel
from starlette import status

config_credentials = dotenv_values(".env")


class TransactionData(BaseModel):
    trans_id: str


def get_transaction(airtimedata):
    if config_credentials["PRODUCTION_STATUS"] == "FALSE":
        base_url = config_credentials["TEST_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}
    else:
        base_url = config_credentials["LIVE_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}

    # datar = {
    #     "trans_id": airtimedata.trans_id,
    # }
    try:
        r = requests.get(url=base_url + "/report?trans_id="+airtimedata.trans_id, headers=headers,)
        data = r.json()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW.Authenticate": "Bearer"}
        )
    return data
