from http.client import HTTPException
import requests
from dotenv import dotenv_values
from pydantic import BaseModel
from starlette import status

from models import Transaction, transaction_pydantic

config_credentials = dotenv_values(".env")


class AirTimeData(BaseModel):
    network: str
    amount: str
    recipent: str
    ported: bool


def get_all_airtime(airtimedata):
    if config_credentials["PRODUCTION_STATUS"] == "FALSE":
        base_url = config_credentials["TEST_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}
    else:
        base_url = config_credentials["LIVE_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}

    datar = {
        "network": airtimedata.network,
        "amount": airtimedata.amount,
        "recipent": airtimedata.recipent,
        "ported": airtimedata.ported
    }
    try:
        r = requests.post(url=base_url + "/airtime", params=datar, headers=headers, )
        data = r.json()

    except:
        return {
            "message": "Transaction failed"
        }

    return data
