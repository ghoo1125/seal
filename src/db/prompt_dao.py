from gettext import find

from .mongodb_client import MongoClientFactory


class PromptDao():
    def __init__(self):
        self.client = MongoClientFactory.get_instance().client
        self.__collection = self.client.database.prompt_collection

    def savePrompt(self, prompt):
        return self.__collection.update_one({"user_id": prompt["user_id"]}, {"$set": prompt}, True)

    def getPromptByUser(self, user_id):
        return self.__collection.find_one({"user_id": user_id})

    def deletePromptByUser(self, user_id):
        return self.__collection.delete_one({"user_id": user_id})
