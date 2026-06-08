import time

import pytest

from pages.CarBase import CarBase
from pages.HomePage import HomePage
from pages.NewCarsPage import NewCarsPage
from testcases.BaseTest import BaseTest
import allure

from utilities import dataProvider


class Test_CarWale(BaseTest):

    @pytest.mark.smoke
    @allure.feature("Find New Cars Test")
    @allure.severity(allure.severity_level.MINOR)
    def test_finding_new_cars(self,page):
        with allure.step("*****Executing Finding New Cars Test*****"):
            home = HomePage(page)
            home.find_new_cars()
            time.sleep(3)


    @allure.feature("Select Cars Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("carBrand,carTitle",dataProvider.get_data("NewCarsTest"))
    def test_select_cars(self,page,carBrand,carTitle):
        with allure.step("*****Executing Select Cars Test*****"):
            home = HomePage(page)
            car = CarBase(page)

            print(f"Car brand is {carBrand}")
            if carBrand == "BMW":
                home.find_new_cars().go_to_BMW()
            elif carBrand == "MG":
                home.find_new_cars().go_to_MG()
            elif carBrand == "Honda":
                home.find_new_cars().go_to_honda()
            elif carBrand == "Toyota":
                home.find_new_cars().go_to_toyota()

            title = car.get_title()
            print(f"Car Title is {title}")
            assert title == carTitle, "Not on the correct page as the title is not matching"

            time.sleep(3)

    @allure.feature("Select Cars Test")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("carBrand,carTitle", dataProvider.get_data("NewCarsTest"))
    def test_print_car_name_prices(self, page, carBrand, carTitle):
        with allure.step("*****Executing Car Name and Price Test*****"):
            home = HomePage(page)
            car = CarBase(page)

            print(f"Car brand is {carBrand}")
            if carBrand == "BMW":
                home.find_new_cars().go_to_BMW()
            elif carBrand == "MG":
                home.find_new_cars().go_to_MG()
            elif carBrand == "Honda":
                home.find_new_cars().go_to_honda()
            elif carBrand == "Toyota":
                home.find_new_cars().go_to_toyota()

            title = car.get_title()
            print(f"Car Title is {title}")
            #assert title == carTitle, "Not on the correct page as the title is not matching"
            car.get_car_name_and_prices()
            time.sleep(1)

