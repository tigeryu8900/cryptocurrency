import json

from util import JsonSerializable


class Transaction(JsonSerializable):
    def __intit__(self, sender):
        self.sender = sender


class TransferTxn(Transaction):
    def __init__(self, sender, receiver, amount):
        super().__intit__(self, sender)
        self.receiver = receiver
        self.amount = amount


