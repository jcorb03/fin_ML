import ibapi

from ibapi.client import EClient #requests info
from ibapi.wrapper import EWrapper #processes received data
from time import sleep
from config import host, port, client_id, ib_account
from threading import Thread

class TradeApp(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.account_id = None
        self.account_value = None

    def nextValidId(self, orderId):
        self.next_order_id = orderId
        print(f"API ready. Next order ID: {orderId}")
        self.reqAccountUpdates(True, ib_account)

    def updateAccountValue(self, key, val, currency, accountName):
        print(f"{key}: {val} {currency}")
        

    def managedAccounts(self, accountsList):
        print("My account ID:", accountsList)

if __name__ == "__main__":
    app = TradeApp()
    app.connect(host, port, client_id)
    app.run()
    
    

    