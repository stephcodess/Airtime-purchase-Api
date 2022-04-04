from tortoise import Model, fields
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True, index=True, unique=True, null=False, generated=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    balance = fields.FloatField(null=False, default=0.0)
    status = fields.CharField(null=False, default="user", max_length=5,)
    password = fields.CharField(max_length=100, null=False)
    transaction_id = fields.CharField(max_length=20, null=False, unique=True, default=0)
    type = fields.CharField(max_length=20, null=False, unique=True, default="airtime")
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow())


user_pydantic = pydantic_model_creator(User, name="user", exclude=("is_verified",))

user_pydantic_log = pydantic_model_creator(User, name="userLogin", exclude=("is_verified", "join_date", "email",
                                                                            "transaction_id"),
                                           exclude_readonly=True)
update_balance_log = pydantic_model_creator(User, name="updateBalance", exclude=("is_verified", "username", "join_date",
                                                                             "id", "status", "password", "join_date",
                                                                             ))
current_user = pydantic_model_creator(User, name="currentUser", exclude=("is_verified", "transaction_id", "username",
                                                                         "join_date", "id",
                                                                         "status", "password", "join_date", "balance"))
user_pydanticIn = pydantic_model_creator(User, name="userIn", exclude=("is_verified", "join_date", "transaction_id",),
                                         exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name="userOut", exclude=("password",))


class Post(Model):
    id = fields.IntField(pk=True, index=True, unique=True, null=False, generated=True)
    title = fields.CharField(max_length=20, null=False, unique=True)
    body = fields.CharField(max_length=200, null=False)
    image = fields.CharField(max_length=200, null=False)
    user_id = fields.CharField(max_length=100, null=False)
    published = fields.BooleanField(default=False)
    created_date = fields.DatetimeField(default=datetime.utcnow())


post_pydantic = pydantic_model_creator(Post, name="post")


class Product(Model):
    id = fields.IntField(pk=True, index=True, unique=True, null=False, generated=True,)
    name = fields.CharField(max_length=20, null=False, unique=True,)
    description = fields.CharField(max_length=200, null=False, unique=True,)
    amount = fields.CharField(max_length=200, null=False, unique=False,)
    user_id = fields.CharField(max_length=100, null=False,)
    published = fields.BooleanField(default=False,)
    created_date = fields.DatetimeField(default=datetime.utcnow())


product_pydantic = pydantic_model_creator(Product, name="product")


class Transaction(Model):
    id = fields.IntField(pk=True, index=True, unique=True, null=False, generated=True,)
    email = fields.CharField(max_length=200, null=False, unique=False)
    type = fields.CharField(max_length=20, null=False, unique=False,)
    transaction_id = fields.CharField(max_length=20, null=False, unique=False,)
    amount = fields.CharField(max_length=200, null=False, unique=False,)
    date = fields.DatetimeField(default=datetime.utcnow())


transaction_pydantic = pydantic_model_creator(Transaction, name="transaction", exclude=("date", "id",))
get_all_transactions = pydantic_model_creator(Transaction, name="all_transaction", exclude=("date", "id", "type",
                                                                                            "amount", "transaction_id"))
