from typing import Optional

from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.signals import post_save
from tortoise.expressions import F

from models import *
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Request, status, Depends

# Authentication
from authentication import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from emailTemp import *
from fastapi.responses import HTMLResponse

# image uploads
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

# Transaction
from vend.airtime.lookup import AirTimeData, get_all_airtime
from vend.data.lookup import DataLookup
from vend.electricity.electricity import electricity_validation, Electricity, purchase_electricity, Purchase
from vend.report import TransactionData, get_transaction

app = FastAPI()

# oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# static files setup config
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post('/token')
async def generate_token(user: user_pydantic_log):
    token = await token_generator(user.username, user.password)
    try:
        payload = jwt.decode(token, config_credentials["SECRET"], algorithms=['HS256'])
        user = await User.get(id=payload.get("id"))
        return {
            "data": {
                "status": "ok",
                "access_token": token,
                "token_type": "bearer",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "verified": user.is_verified,
                    "joined_date": user.join_date.strftime("%b %d %Y")
                }
            }
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or User",
            headers={"WWW.Authenticate": "Bearer"}
        )


# @post_save(User)
# async def create_user(
#     sender: "Type[User]",
#     instance: User,
#     created: bool,
#     using_db: "Optional[BaseDBAsyncClient]",
#     update_fields: List[str]
# ) -> None:
#     if created:
#         await send_email([instance.email], instance)

@app.get("/users")
async def all_users():
    user = await User.all()
    return user if len(user) != 0 else "No registered user."


@app.get("/delete-user")
async def delete_user():
    user = await User.all()
    return user if len(user) != 0 else "No registered user."


@app.post("/current-user")
async def get_current_logged_in_user(current: current_user):
    user = await User.get(email=current.email)
    return user


@app.post("/register")
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status": "registered",
        "data": {
            "message": f"Hello {new_user.username}, thanks for choosing us"
        }
    }


@app.get("/verication", response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return {
            "status": "Account verification successful"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
        headers={"WWW.Authenticate": "Bearer"}
    )


@app.post("/validate-electricity")
async def validate_electricity(params: Electricity):
    validate = electricity_validation(params)
    return validate


@app.post("/purchase-electricity")
async def vend_electricity(params: Purchase):
    purchase = purchase_electricity(params)
    return purchase


@app.post("/vend/airtime")
async def get_airtime_lookups(params: AirTimeData):

    vendairtime = get_all_airtime(params)
    return {
        "details": vendairtime
    }

@app.post("/transaction-details")
async def get_transaction_details(params: TransactionData):
    transaction = await get_transaction(params)
    return {
        "details": transaction
    }


@app.post("/transactions")
async def get_all_transactions_by_user(params: get_all_transactions):
    transactions = await Transaction.filter(email=params.email)
    if transactions:
        return transactions
    else:
        return {
            {"message": "You haven't made any transaction"},
            {"message": "You haven't made any transaction"}
        }


@app.get("/all-transaction")
async def get_all_transactions_by_user():
    transactions = await Transaction.all()
    return transactions


@app.post("/lookup/data")
async def lookup_data(params: DataLookup):
    lookup = lookup_data(params.dict())
    return {
        "details": lookup
    }


@app.post("/create-post")
async def create_post(post: post_pydantic, file: UploadFile = File(...)):
    filePath = "./static/images"
    fileName = file.filename
    extension = fileName.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        return {
            "status": "error",
            "detail": "The file extension is not supported"
        }
    token_name = secrets.token_hex(10) + "." + extension
    generated_name = filePath + token_name
    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)

    # Pillow
    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)
    file.close()

    post_info = post.dict(exclude_unset=True)
    post_obj = await Post.create(**post_info)
    new_post = await post_pydantic.from_tortoise_orm(post_obj)
    return new_post


async def create_transaction(transaction: transaction_pydantic):
    transaction_info = transaction
    transaction_obj = await Transaction.create(**transaction_info)
    new_transaction = await transaction_pydantic.from_tortoise_orm(transaction_obj)
    return new_transaction


@app.post("/update-balance")
async def update_balance(data: update_balance_log):
    user = await User.get(email=data.email)
    if user:
        if user.balance >= data.balance:
            updated = await User.filter(email=user.email).update(balance=user.balance - data.balance, transaction_id=data.transaction_id)
            transaction = await create_transaction({'email': data.email, 'type': data.email, 'amount': data.balance,
                                                    "transaction_id": data.transaction_id})
            return updated
    else:
        updated = {
            "meessage": "Insufficient Balance. Top up your Wallet."
        }
        return updated


@app.post("/")
async def hello_world():
    return "hello world"
# @app.get("/transactions")
# async def create_transaction(transaction: transaction_pydantic):
#     transaction_info = transaction.dict()
#     transaction_obj = await Transaction.create(**transaction_info)
#     new_transaction = await transaction_pydantic.from_tortoise_orm(transaction_obj)
#     return new_transaction

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://fidpress-api.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
