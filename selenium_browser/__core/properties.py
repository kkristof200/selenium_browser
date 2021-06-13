# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional

# Pip
from kproxy import Proxy

from selenium.webdriver.remote.webdriver import WebDriver

# Local
from ..models import Capabilities

# -------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------- class: Properties ------------------------------------------------------ #

class Properties:

    # --------------------------------------------------- Public properties -------------------------------------------------- #

    driver: WebDriver


    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def proxy(self) -> Optional[Proxy]:
        return self._proxy

    @property
    def capabilities(self) -> Capabilities:
        return Capabilities(self.driver.capabilities)


    # -------------------------------------------------- Private properties -------------------------------------------------- #

    _user_agent: Optional[str]
    _proxy     : Optional[Proxy]


# -------------------------------------------------------------------------------------------------------------------------------- #