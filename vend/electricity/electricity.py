from http.client import HTTPException
import requests
from dotenv import dotenv_values
from pydantic import BaseModel
from starlette import status

config_credentials = dotenv_values(".env")


class Electricity(BaseModel):
    meter_number: str
    meter_type: str
    amount: str
    service: str


class Purchase(BaseModel):
    productCode: str
    productToken: str
    phone: str


def electricity_validation(electricity):
    if config_credentials["PRODUCTION_STATUS"] == "FALSE":
        base_url = config_credentials["TEST_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}
    else:
        base_url = config_credentials["LIVE_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}

    datar = {
        "meter_number": electricity.meter_number,
        "meter_type": electricity.meter_type,
        "amount": electricity.amount,
        "service": electricity.service
    }

    try:
        r = requests.post(url=base_url + "/electricity/validate", params=datar, headers=headers,)
        data = r.json()

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW.Authenticate": "Bearer"}
        )
    return data


def purchase_electricity(electricity):
    if config_credentials["PRODUCTION_STATUS"] == "FALSE":
        base_url = config_credentials["TEST_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}
    else:
        base_url = config_credentials["LIVE_BASE_URL"]
        headers = {"Authorization": "Bearer " + config_credentials["TEST_TOKEN"]}

    datar = {
        "productCode": electricity.productCode,
        "productToken": electricity.productToken,
        "phone": electricity.phone
    }

    try:
        r = requests.post(url=base_url + "/electricity/vend", params=datar, headers=headers,)
        data = r.json()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW.Authenticate": "Bearer"}
        )
    return data