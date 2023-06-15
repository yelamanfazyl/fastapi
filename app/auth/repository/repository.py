from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        return self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def add_favorite_shanyrak(self, user_id: str, shanyrak_id: str):
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$push": {
                    "favorites": ObjectId(shanyrak_id),
                }
            },
        )

    def get_favorite_shanyraks(self, user_id: str):
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )

        if user is None:
            return None

        if "favorites" not in user:
            return None

        return user["favorites"]

    def delete_favorite_shanyrak(self, user_id: str, shanyrak_id: str):
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$pull": {
                    "favorites": ObjectId(shanyrak_id),
                }
            },
        )

    def add_avatar(self, user_id: str, avatar: str):
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "avatar": avatar,
                }
            },
        )

    def delete_avatar(self, user_id: str):
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "avatar": "",
                }
            },
        )

    def get_avatar_url(self, user_id: str):
        user = self.database["users"].find_one(
            filter={"_id": ObjectId(user_id)},
        )

        if user is None:
            return None

        if "avatar" not in user:
            return None

        if user["avatar"] == "":
            return None

        return user["avatar"]
