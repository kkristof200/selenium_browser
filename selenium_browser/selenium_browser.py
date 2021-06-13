# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional, Union, List, Tuple
import os, shutil, time

# Pip
from noraise import noraise
from kproxy import Proxy

# Local
from .__core import BrowserCookies, FindFuncs, Properties, WebelementFunctions
from .models import Capabilities

from .addons import AddonManager, AddonInstallSettings
from .__resources import Constants
from .utils import Utils

# -------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: Browser -------------------------------------------------------- #

class Browser(
    BrowserCookies,
    FindFuncs,
    Properties,
    WebelementFunctions
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

        # addons
        addons_folder_path: Optional[str] = None,
        addon_settings: Optional[List[AddonInstallSettings]] = None,
        supported_addon_file_extensions: List[str] = ['xpi', 'crx', 'zip'],
        addon_url_format: str = 'PROVIDE_THIS',

        # find function
        default_find_func_timeout: int = 2.5,

        # post init args
        full_screen: bool = False,

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
        self.__proxy = proxy

        self.cookies_folder_path = Utils.cookies_folder_path(
            cookies_folder_path=cookies_folder_path,
            cookies_id=cookies_id
        )
        os.makedirs(self.cookies_folder_path, exist_ok=True)

        if webdriver_executable_path:
            webdriver_kwargs['executable_path'] = webdriver_executable_path

        self.driver = webdriver_class(**webdriver_kwargs)

        if full_screen:
            self.driver.fullscreen_window()

        am = AddonManager(
            self,
            supported_addon_file_extensions=supported_addon_file_extensions,
            addon_url_format=addon_url_format,
        )

        am.install_addons(
            addons_settings=am.get_all_addon_settings(
                addons_folder_path=addons_folder_path,
                user_addon_settings=addon_settings
            ),
            temporary=False
        )


    # --------------------------------------------------- Public properties -------------------------------------------------- #

    @property
    def proxy(self) -> Optional[Proxy]:
        return self.__proxy


    # ------------------------------------------------------ Destructor ------------------------------------------------------ #

    @noraise(print_exc=False)
    def __del__(self):
        if os.path.exists(self.driver.profile.path):
            self.quit()


# -------------------------------------------------------------------------------------------------------------------------------- #