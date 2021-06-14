# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional, Union, List, Tuple, Callable
import os, shutil, time

# Pip
from noraise import noraise
from kproxy import Proxy

# Local
from .core import BrowserCookies, BrowserFindFuncs, BrowserProperties, BrowserWebelementFunctions
from .models import Capabilities

from .__resources import Constants
from .utils import Utils

# -------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: Browser -------------------------------------------------------- #

class Browser(
    BrowserCookies,
    BrowserFindFuncs,
    BrowserProperties,
    BrowserWebelementFunctions
):

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,

        webdriver_class,

        # cookies
        cookies_folder_path: Optional[str] = None,
        cookies_id: Optional[str] = None,
        pickle_cookies: bool = False,

        # proxy
        proxy: Optional[Union[Proxy, str]] = None,

        # find function
        default_find_func_timeout: int = 2.5,

        # webdriver_kwargs
        webdriver_executable_path: Optional[str] = None,
        **webdriver_kwargs
    ):
        '''EITHER PROVIDE 'cookies_id' OR  'cookies_folder_path'.
           IF 'cookies_folder_path' is None, 'cokies_id', will be used to calculate 'cookies_folder_path'
           IF 'cokies_id' is None, the name of the 'profile_path' follder wil lbe used. if that is Nonne too, 'test' will be used
        '''

        self.default_find_func_timeout = default_find_func_timeout
        self.pickle_cookies = pickle_cookies
        self._proxy = proxy

        self.cookies_folder_path = Utils.cookies_folder_path(
            cookies_folder_path=cookies_folder_path,
            cookies_id=cookies_id
        )
        os.makedirs(self.cookies_folder_path, exist_ok=True)

        if webdriver_executable_path:
            webdriver_kwargs['executable_path'] = webdriver_executable_path

        self.driver = webdriver_class(**webdriver_kwargs)


    # ------------------------------------------------------ Destructor ------------------------------------------------------ #

    @noraise(print_exc=False)
    def __del__(self):
        if os.path.exists(self.driver.profile.path):
            self.quit()


# -------------------------------------------------------------------------------------------------------------------------------- #