
import json
import hashlib

class JsonSerializable:
    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)

    def to_json(self):
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
        #return json.dumps(self.__dict__, sort_keys=True)
        return self.__dict__


class Hasher:
    @staticmethod
    def object_hash(obj):
        """
        Calculates the hash of a given object.
        """
        if type(obj) == bytes:
            return hashlib.sha256(obj).hexdigest()
        if type(obj) == str:
            return hashlib.sha256(obj.encode()).hexdigest()
        obj_string = json.dumps(obj.to_json(), sort_keys=True).encode()
        return hashlib.sha256(obj_string).hexdigest()

    @staticmethod
    def hash(data: str):
        """
        Calculates the hash of a given string.
        """
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def raw_hash(data1, data2 = None):
        """
        Calculates the hash of a given string.
        """
        h = hashlib.sha256()
        h.update(data1)
        if data2 is not None: h.update(data2)
        return h.digest()
