import os
import json
import uuid
from typing import Any

class DataStoreItem:
    id: str = None
    data: dict = None
    path: str = None
    table: str = None
    
    def __init__(self, id: str, data: dict, path: str, table: str) -> None:
        self.id = id
        self.data = data
        self.path = path
        self.table = table
    
    def delete(self) -> None:
        os.remove(self.path)

class DataStore:
    path: str = None
    data: list[DataStoreItem] = []
    database: Any = None
    
    def __init__(self, path: os.PathLike | str, database: Any = None) -> None:
        self.path = path
        self.database = database
    
    def add(self, data: dict, id: str = uuid.uuid4().hex) -> DataStoreItem:
        filepath = os.path.join(self.path, id)
        with open(filepath, "w") as file:
            file.write(json.dumps(data))
        item = DataStoreItem(id, data, filepath)
        self.data.append(item)
        return item
    
    def add_unique(self, data: dict, id: str = uuid.uuid4().hex) -> None:
        if any(item.data == data for item in self.data):
            return
        self.add(data, id)
    
    def get(self, id: str) -> DataStoreItem:
        filepath = os.path.join(self.path, id)
        with open(filepath, "r") as file:
            return DataStoreItem(file.name, json.loads(file.read()), filepath)
    
    def delete(self, id: str) -> None:
        fn = os.path.join(self.path, id)
        os.remove(fn)
        self.load()
    
    def clear(self) -> None:
        for item in self.data:
            item.delete()
        self.data = []
    
    def list(self) -> list[str]:
        return [os.path.splitext(f)[0] for f in os.listdir(self.path)]
    
    def load(self):
        self.data = []
        for f in self.list():
            self.data.append(self.get(f))
    
    def commit(self) -> None:
        self.load()
        self.database.commit(self.data)
        self.clear()