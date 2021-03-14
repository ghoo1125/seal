import pprint
from gettext import find

from mongodb_client import MongoClientFactory


class PromptDao:
    def __init__(self, client):
        self.__collection = client.database.prompt_collection

    def savePrompt(self, prompt):
        return self.__collection.insert_one(prompt).inserted_id

    def getPromptById(self, id):
        return self.__collection.find_one({"_id": id})

    def getPromptsByUser(self, userId):
        return self.__collection.find({"userId": userId})

if __name__ == "__main__":
    client = MongoClientFactory.get_instance().client
    dao = PromptDao(client)
    prompt = {"userId": "Louis", "hints": [{"question": "Facebook", "answer": "Bb***"}]}
    id = dao.savePrompt(prompt)
    record = dao.getPromptById(id)
    records = dao.getPromptsByUser("Louis")
    pprint.pprint(record)
    for record in records:
        pprint.pprint(record)
