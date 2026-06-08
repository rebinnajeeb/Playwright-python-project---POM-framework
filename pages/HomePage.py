from pages.BasePage import BasePage
from pages.NewCarsPage import NewCarsPage


class HomePage(BasePage):

    def __init__(self, page):
       super().__init__(page)

    def find_new_cars(self):
        self.move_to("newCar_XPATH")
        self.click("findNewCars_XPATH")

        return NewCarsPage(self.page)

    def go_to_used_cars(self):
        pass

    def go_to_search_cars(self):
        pass

