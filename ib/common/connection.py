from ib.ib import IBapi
from ib.common.account import Account


class IBConnection:
    def __init__(
        self, ip: str = "127.0.0.1", port: int = 4002, client_id: int = 200
    ) -> None:
        self._ip = ip
        self._port = port
        self._client_id = client_id
        self._ibapi = IBapi()

    def open(self):
        self._ibapi.open(self._ip, self._port, self._client_id)

    def close(self):
        self._ibapi.close()

    def __enter__(self):
        self.open()

    def __exit__(self, *args):
        self.close()

    def accounts(self) -> list[Account]:
        self._ibapi.reqManagedAccts()
        
