from pymongo import MongoClient, errors


class MongoClientFactory():
    __DOMAIN = 'localhost'
    __PORT = 27017
    __instance = None

    @staticmethod
    def get_instance():
        if MongoClientFactory.__instance is None:
            MongoClientFactory.__instance = MongoClientFactory(
                MongoClientFactory.__instance)
        return MongoClientFactory.__instance

    def __init__(self, instance):
        assert(instance == MongoClientFactory.__instance)
        try:
            self.client = MongoClient(
                host=[str(MongoClientFactory.__DOMAIN) + ":" +
                      str(MongoClientFactory.__PORT)],
                serverSelectionTimeoutMS=3000,  # 3 second timeout
            )
            print("initialize mongo client")
        except errors.ServerSelectionTimeoutError as err:
            self.client = None
            print("pymongo ERROR:", err)
