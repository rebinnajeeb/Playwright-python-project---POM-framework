from utilities import configReader
import logging
import allure

from utilities.LogUtil import Logger

log = Logger(__name__,logging.INFO)

class BasePage:

    def __init__(self,page):
        self.page = page

    def click(self, locator):
        with allure.step(f"Clicking on an Element {locator}"):
          self.page.locator(configReader.readConfig("locators",locator)).click()
          log.logger.info(f"Clicking on an Element {locator}")

    def type(self, locator, value):
        with allure.step(f"Typing in an Element {locator} and entered value as {value}"):
          self.page.locator(configReader.readConfig("locators",locator)).fill(value)
          log.logger.info(f"Typing in an Element {locator} and entered value as {value}")

    def move_to(self, locator):
        with allure.step(f"Moving to an Element {locator}"):
          self.page.locator(configReader.readConfig("locators",locator)).hover()
          log.logger.info(f"Moving to an Element {locator}")
