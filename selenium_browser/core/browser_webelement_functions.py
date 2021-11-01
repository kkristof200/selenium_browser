# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional, Tuple, Union, List
import random, time, copy
from sys import platform

# Pip
from noraise import noraise

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Local
from .browser_js_functions import BrowserJSFunctions

# -------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------- class: BrowserWebelementFunctions ---------------------------------------------- #

class BrowserWebelementFunctions(BrowserJSFunctions):

    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

    @noraise()
    def get_attribute(self, element, key: str) -> Optional[str]:
        return element.get_attribute(key)

    def set_textfield_text_remove_old(
        self,
        element: WebElement,
        text: str
    ) -> bool:
        try:
            element.click()
        except:
            pass

        time.sleep(0.5)
        element.clear()
        element.send_keys(Keys.BACK_SPACE)

        try:
            time.sleep(0.5)
            element.send_keys(Keys.COMMAND if platform == 'darwin' else Keys.CONTROL, 'a')
            time.sleep(0.5)
            element.send_keys(Keys.BACK_SPACE)
        except Exception as e:
            print(e)

        time.sleep(0.5)
        element.send_keys('a')
        time.sleep(0.5)
        element.send_keys(Keys.BACK_SPACE)

        time.sleep(0.5)

        element.send_keys(text)

        return True

    @noraise(default_return_value=False)
    def send_keys_delay_random(
        self,
        element: WebElement,
        keys: Union[str, int, float, List[str], List[int], List[float]],
        min_delay: float = 0.025,
        max_delay: float = 0.25
    ) -> bool:
        _keys = copy.deepcopy(keys)

        if type(_keys) in [int, float]:
            _keys = str(_keys)

        for key in _keys:
            if type(key) in [int, float]:
                key = str(key)

            element.send_keys(key)
            time.sleep(random.uniform(min_delay,max_delay))

        return True

    @noraise(default_return_value=False)
    def scroll_to_element(self, element, header_element=None) -> bool:
        header_h = 0

        if header_element is not None:
            _, _, _, header_h, _, _ = self.get_element_coordinates(header_element)

        _, element_y, _, _, _, _ = self.get_element_coordinates(element)

        return self.scroll_to(element_y-header_h)

    def scroll_to_bottom(self, steps_pixels: int = 1000) -> None:
        MAX_TRIES = 25
        SCROLL_PAUSE_TIME = 0.5
        current_tries = 1
        last_height = 0

        while True:
            self.scroll(steps_pixels)
            time.sleep(SCROLL_PAUSE_TIME)
            current_height = self.current_page_offset_y()

            if last_height == current_height:
                current_tries += 1

                if current_tries == MAX_TRIES:
                    break
                else:
                    continue
            else:
                current_tries = 1

            last_height = current_height


    @noraise(default_return_value=False)
    def move_to_element(
        self,
        element: Optional[WebElement],
        offset: Optional[Tuple[int, int]] = None,
        click: bool = False
    ) -> bool:
        if not element:
            print('move_to_element: None element passed')

            return False

        ac = ActionChains(self.driver)
        ac.move_to_element_with_offset(element, offset[0], offset[1]) if offset else ac.move_to_element(element)

        if click:
            ac.click()

        ac.perform()

        return True

    @noraise(default_return_value=False)
    def switch_to_frame(self, iframe: Optional[WebElement]) -> bool:
        if not iframe:
            print('switch_to_frame: None frame passed')

            return False

        self.driver.switch_to.frame(iframe)

        return True

    # returns x, y, w, h, max_x, max_y
    def get_element_coordinates(self, element: WebElement) -> Tuple[int, int, int, int, int, int]:
        location = element.location
        size = element.size

        x = location['x']
        y = location['y']
        w = size['width']
        h = size['height']

        return x, y, w, h, x+w, y+h


# -------------------------------------------------------------------------------------------------------------------------------- #