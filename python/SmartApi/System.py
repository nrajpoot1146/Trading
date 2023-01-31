from smartapi import SmartConnect
import zope.interface


class MainSystem:
    def __init__(self, ClientCode, Pin):
        self.ClientCode = ClientCode
        self.Pin = Pin
        self.obj = SmartConnect(api_key="l5g7IX0d")

    def login(self, totp: str):
        self.data = self.obj.generateSession(self.ClientCode, self.Pin, totp)
        pass

    def logout(self):
        logout = self.obj.terminateSession(self.ClientCode)
        print("Logout Successfull")
        pass

    def getRefereshToken(self):
        return self.data['data']['refreshToken']


class Api(zope.interface.Interface):
    pass
