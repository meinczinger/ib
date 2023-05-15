from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.account_summary_tags import AccountSummaryTags
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def managedAccounts(self, accounts_list: str):
        super().managedAccounts(accounts_list)
        print("Account list:", accounts_list)


def test_account_details():
    print("creating api")
    app = IBapi()
    print("Connecting")
    app.connect("127.0.0.1", 4002, 126)
    app.run()
    time.sleep(5)
    app.reqManagedAccts()
    time.sleep(2)
    app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)
    app.disconnect()
    print("done")


test_account_details()
