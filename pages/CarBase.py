from utilities import configReader


class CarBase:

    def __init__(self,page):
        self.page = page


    def get_title(self):
        return self.page.locator(configReader.readConfig("locators","carTitle_XPATH")).inner_text()

    def get_car_name_and_prices(self):
        carNames = self.page.locator(configReader.readConfig("locators","carName_XPATH"))
        carPrices = self.page.locator(configReader.readConfig("locators","carPrice_XPATH"))
        print(f"Car prices length is {carPrices}")

        for i in range(1, carPrices.count()):
            print(carNames.nth(i).inner_text()+"----prices are--"+carPrices.nth(i).inner_text())