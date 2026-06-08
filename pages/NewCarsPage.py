from pages.BMWCarsPage import BMWCarsPage
from pages.BasePage import BasePage
from pages.HondaCarsPage import HondaCarsPage
from pages.MGCarsPage import MGCarsPage
from pages.ToyotaCarsPage import ToyotaCarsPage


class NewCarsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def go_to_toyota(self):
        self.click("toyota_XPATH")
        return ToyotaCarsPage(self.page)

    def go_to_BMW(self):
        self.click("Bmw_XPATH")
        return BMWCarsPage(self.page)

    def go_to_honda(self):
        self.click("honda_XPATH")
        return HondaCarsPage(self.page)

    def go_to_MG(self):
        self.click("MG_XPATH")
        return MGCarsPage(self.page)