from ibapi.client import EClient, Decimal, TickerId, Contract, ListOfContractDescription
from ibapi.wrapper import EWrapper, RealTimeBar, TickTypeEnum
from ibapi.account_summary_tags import AccountSummaryTags
import time
import threading
from datetime import datetime


class ContractSamples:

    """Usually, the easiest way to define a Stock/CASH contract is through
    these four attributes."""

    @staticmethod
    def EurGbpFx():
        #! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "GBP"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def open(self, ip, port, client_id):
        self.connect(ip, port, client_id)
        self.run()

    def close(self):
        self.disconnect()

    def managedAccounts(self, accounts_list: str):
        super().managedAccounts(accounts_list)

    def realtimeBar(
        self,
        reqId: TickerId,
        time: int,
        open_: float,
        high: float,
        low: float,
        close: float,
        volume: Decimal,
        wap: Decimal,
        count: int,
    ):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        print(
            "RealTimeBar. TickerId:",
            reqId,
            RealTimeBar(time, -1, open_, high, low, close, volume, wap, count),
        )

    def tickPrice(self, reqId, tickType, price, attrib):
        print(
            f"tickPrice reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}"
        )

    def historicalData(self, reqId, bar):
        print(
            # f"Time: {datetime.fromtimestamp(int(bar.date))} Open: {bar.open} Close: {bar.close} Low: {bar.low} High: {bar.high}"
            f"Time: {bar.date} Open: {bar.open} Close: {bar.close} Low: {bar.low} High: {bar.high}"
        )

    def symbolSamples(
        self, reqId: int, contractDescriptions: ListOfContractDescription
    ):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol Samples. Request Id: ", reqId)

        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += " "
                derivSecTypes += derivSecType
                print(
                    "Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
                    "currency:%s, derivativeSecTypes:%s, description:%s, issuerId:%s"
                    % (
                        contractDescription.contract.conId,
                        contractDescription.contract.symbol,
                        contractDescription.contract.secType,
                        contractDescription.contract.primaryExchange,
                        contractDescription.contract.currency,
                        derivSecTypes,
                        contractDescription.contract.description,
                        contractDescription.contract.issuerId,
                    )
                )


def run_loop():
    app.run()


print("creating api")
app = IBapi()

print("Connecting")
app.connect("127.0.0.1", 4002, 131)
print("running")
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()
time.sleep(2)
print("requesting")
apple_contract = Contract()
apple_contract.symbol = "AAPL"
apple_contract.secType = "STK"
apple_contract.exchange = "SMART"
apple_contract.currency = "USD"
# app.reqMatchingSymbols(218, "AAPL")
# Request Market Data
app.reqMarketDataType(3)
# app.reqMktData(1, apple_contract, "", 0, 0, [])
app.reqHistoricalData(1, apple_contract, "", "3 M", "1 day", "TRADES", 1, 2, False, [])

# app.reqRealTimeBars(3001, ContractSamples.EurGbpFx(), 5, "MIDPOINT", True, [])
# app.reqManagedAccts()
# app.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)
print("requested")
time.sleep(5)
app.cancelRealTimeBars(3001)
app.disconnect()
print("done")
