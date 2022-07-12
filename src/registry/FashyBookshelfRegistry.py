from Registry import Registry

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from multiprocessing import (
  Lock
)

def setup_state(registry, driver):
  registry.last_known_video_index = 0
  registry.video_list = driver.find_elements(
    By.CSS_SELECTOR,
    ".channel-videos-image"
  )
  driver.click(registry.video_list[0])
  registry.last_known_video_index += 1

class FashyBookshelfRegistry(Registry):
  def __init__(self, _driver) -> None:
    super().__init__("https://www.bitchute.com/channel/n5KVFNEswHtE/", _driver)
    setup_state(self, _driver)

  def is_up_to_date(_target):
    return False

  def get_tranche_of_targets(self, driver):

  def setup_state(self, driver):
    self.last_known_video_index = 0


  def to_next_tranche_of_targetS(self, driver):
    driver.back()
    driver.click(self.video_list[self.last_known_video_index])
    self.last_known_video_index += 1
