# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import Optional, List
import os

# Local
from .models import AddonInstallSettings

# -------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: AddonManager ----------------------------------------------------- #

class AddonManager:

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,

        browser, #: Firefox, Chrome, etc.

        supported_addon_file_extensions: List[str],
        addon_url_format = str
    ):
        self.browser = browser

        self.__supported_addon_file_extensions = supported_addon_file_extensions
        self.__addon_url_format = addon_url_format


    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

    def get_all_addon_settings(
        self,
        addons_folder_path: Optional[str] = None,
        user_addon_settings: Optional[List[AddonInstallSettings]] = None,
        lib_addon_settings: Optional[List[AddonInstallSettings]] = None
    ) -> List[AddonInstallSettings]:
        addon_settings = lib_addon_settings or []

        if user_addon_settings:
            addon_settings.extend(user_addon_settings)

        if addons_folder_path and os.path.exists(addons_folder_path):
            addon_settings.extend(self.addons_from_folder(addons_folder_path))

        return addon_settings

    def addons_from_folder(
        self,
        folder_path: str
    ) -> List[AddonInstallSettings]:
        for (dirpath, _, filenames) in os.walk(folder_path):
            return [
                AddonInstallSettings(os.path.join(dirpath, f))
                for f in filenames if f.split('.')[-1] in self.__supported_addon_file_extensions
            ]

    def install_addons(
        self,
        addons_settings: List[AddonInstallSettings],
        temporary: Optional[bool] = False
    ) -> List[Optional[str]]:
        return [
            self.install_addon(addon_settings=addon_settings, temporary=temporary)
            for addon_settings in addons_settings
        ]

    def install_addon(
        self,
        addon_settings: AddonInstallSettings,
        temporary: Optional[bool] = False,
        debug: bool = False
    ) -> Optional[str]:
        if addon_settings.path.split('.')[-1] not in self.__supported_addon_file_extensions:
            if debug:
                print('Will not install \'{}\'. Reason: not one of the needed formats: {}'.format(
                    addon_settings.path,
                    self.__supported_addon_file_extensions
                ))

            return None

        org_handle = self.browser.driver.current_window_handle
        addon_id = self.browser.driver.install_addon(addon_settings.path, temporary=temporary)

        if not addon_id:
            if debug:
                print('Could not install addon with path \'{}\''.format(addon_settings.path))

                return None

        if debug:
            print('Did install addon with id \'{}\' and path \'{}\''.format(addon_id, addon_settings.path))

        internal_addon_id = self.get_addon_internal_id(addon_id)
        org_current_url = self.browser.current_url

        def reset(org_handle, org_current_url):
            if len(self.browser.window_handles) > 1:
                for handle in self.browser.window_handles:
                    self.browser.switch_to_window(handle)

                    if internal_addon_id in self.browser.current_url:
                        self.browser.close()

                        return reset(org_handle, org_current_url)

            if org_handle not in self.browser.window_handles:
                org_handle = self.browser.window_handles[0]

            self.browser.switch_to_window(org_handle)
            self.browser.get(org_current_url)

        reset(org_handle, org_current_url)

        addon_settings.post_install_action(
            self.browser,
            addon_id,
            internal_addon_id,
            self.__addon_url_format.format(internal_addon_id)
        )

        reset(org_handle, org_current_url)

        return addon_id


    # ---------------------------------------------------- Private methods --------------------------------------------------- #

    def get_addon_internal_id(
        self,
        addon_public_id: str
    ) -> Optional[str]:
        return addon_public_id


# -------------------------------------------------------------------------------------------------------------------------------- #