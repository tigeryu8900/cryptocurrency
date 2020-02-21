
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
    def object_hash(block_header):
        """
        Calculates the hash of a given object.
        """
        obj_string = json.dumps(block_header.to_json(), sort_keys=True).encode()
        return hashlib.sha256(obj_string).hexdigest()

    @staticmethod
    def hash(data: str):
        """
        Calculates the hash of a given string.
        """
        return hashlib.sha256(data.encode()).hexdigest()
