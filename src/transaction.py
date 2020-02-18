from src.util import JsonSerializable


class Transaction(JsonSerializable):
    def __intit__(self, sender: str):
        self.sender = sender


# This is the balance transfer transaction, we could support more other types of transaction later.
class TransferTxn(Transaction):
    def __init__(self, sender: str, receiver: str, amount: int):
        super().__intit__(sender)
        self.receiver = receiver
        self.amount = amount

