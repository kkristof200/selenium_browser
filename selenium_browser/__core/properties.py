# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from kproxy import Proxy

from selenium.webdriver.remote.webdriver import WebDriver

# Local
from .js_functions import JSFunctions
from ..models import Capabilities

# -------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: Properties ------------------------------------------------------ #

class Properties(JSFunctions):

    # --------------------------------------------------- Public properties -------------------------------------------------- #

    driver: WebDriver


    @property
    def user_agent(self) -> str:
        return self.js_get_user_agent()

    @property
    def proxy(self) -> Optional[Proxy]:
        return self._proxy

    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(self.driver.capabilities)


    # -------------------------------------------------- Private properties -------------------------------------------------- #

    _proxy     : Optional[Proxy]


# -------------------------------------------------------------------------------------------------------------------------------- #