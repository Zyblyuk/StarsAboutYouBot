import pickle
import os
class Users:
    def __init__(self, DataBase):
        self.users = {}
        self.temp_users = {}
        self.temp_list = {}
        self.FileName = DataBase
        if not os.path.getsize(self.FileName) :
            with open(self.FileName, "wb") as fh:
                pickle.dump(self.users, fh)
        with open(self.FileName, "rb") as fh:
            self.users = pickle.load(fh)
    def save(self):
        with open(self.FileName, "wb") as fh:
            pickle.dump(self.users, fh)
    def add(self, chat_id, elem):
        temp = []
        if chat_id in self.users:
            temp = self.users[chat_id]
            temp.append(elem)
            self.users[chat_id] = temp
            self.save()
        else:
            temp.append(elem)
            self.users[chat_id] = temp

    def temp_add(self, chat_id, elem):
        temp = []
        if chat_id in self.temp_users:
            temp = self.temp_users[chat_id]
            temp.append(elem)
            self.temp_users[chat_id] = temp
        else:
            temp.append(elem)
            self.temp_users[chat_id] = temp
