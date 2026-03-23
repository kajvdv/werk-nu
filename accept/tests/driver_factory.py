from accept.drivers import Driver
from accept.drivers.http import HttpDriver
from accept.drivers.selenium import SeleniumDriver
from storyteller import DriverFactory


class HttpDriverFactory(DriverFactory):
    def create_driver(self) -> Driver:
        return HttpDriver()

class SeleniumDriverFactory(DriverFactory):
    def __init__(self) -> None:
        self.i = 0
    
    def _get_next_port(self) -> int:
        ports = [9222, 9223] # Stupid, I know
        port = ports[self.i]
        self.i += 1
        return port
    
    def create_driver(self) -> Driver:
        return SeleniumDriver(self._get_next_port())