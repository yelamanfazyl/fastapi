from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database
from typing import Dict


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, input: dict):
        found = self.database["users"].find_one({"_id": ObjectId(input["user_id"])})

        if found is None:
            return None

        payload = {
            "user_id": ObjectId(input["user_id"]),
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
            "location": {
                "lattitude": input["location"][0],
                "longitude": input["location"][1],
            },
            "media": [],
            "comments": [],
            "created_at": datetime.utcnow(),
        }

        result = self.database["shanyraks"].insert_one(payload)

        return str(result.inserted_id)

    def get_shanyrak_by_id(self, id: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        return shanyrak

    def add_shanyrak_media(self, id: str, data: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "media": data,
                }
            },
        )

        return result

    def update_shanyrak_by_id(
        self, id: str, user_id: str, data: dict, location: Dict[str, float]
    ) -> bool:
        found = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
                "user_id": ObjectId(user_id),
            }
        )

        if found is None:
            return False

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$set": {
                    "type": data["type"],
                    "price": data["price"],
                    "address": data["address"],
                    "area": data["area"],
                    "rooms_count": data["rooms_count"],
                    "description": data["description"],
                    "location": {
                        "lattitude": location["lat"],
                        "longitude": location["lng"],
                    },
                }
            },
        )

        return result.modified_count == 1

    def delete_shanyrak_by_id(self, id: str, user_id: str) -> bool:
        found = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
                "user_id": ObjectId(user_id),
            }
        )

        if found is None:
            return False

        result = self.database["shanyraks"].delete_one(
            filter={"_id": ObjectId(id)},
        )

        return result.deleted_count == 1

    def delete_shanyrak_media(self, id: str, data: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$pull": {
                    "media": data,
                }
            },
        )

        return result

    def create_comment(self, id: str, user_id: str, content: str):
        found = self.database["shanyraks"].find_one({"_id": ObjectId(id)})

        if found is None:
            return None

        found = self.database["users"].find_one({"_id": ObjectId(user_id)})

        if found is None:
            return None

        payload = {
            "id": ObjectId(),
            "content": content,
            "author_id": ObjectId(user_id),
            "created_at": datetime.utcnow(),
        }

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "comments": payload,
                }
            },
        )

        return result

    def get_comments(self, id: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        print(shanyrak)

        if shanyrak["comments"] is None:
            return None

        return shanyrak["comments"]

    def delete_comment(self, id: str, comment_id: str, user_id: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        if shanyrak["comments"] is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$pull": {
                    "comments": {
                        "id": ObjectId(comment_id),
                        "author_id": ObjectId(user_id),
                    },
                }
            },
        )

        return result

    def update_comment(self, id: str, comment_id: str, user_id: str, content: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        if shanyrak["comments"] is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={
                "_id": ObjectId(id),
                "comments.id": ObjectId(comment_id),
                "comments.author_id": ObjectId(user_id),
            },
            update={
                "$set": {
                    "comments.$.content": content,
                }
            },
        )

        return result
