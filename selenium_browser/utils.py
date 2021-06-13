# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from  typing import Optional, Dict, Union
import os, tempfile, platform, subprocess

# Pip
from kproxy import Proxy

# Local
from .__resources.constants import Constants

# -------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: Utils --------------------------------------------------------- #

class Utils:

    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

    @staticmethod
    def cookies_folder_path(
        cookies_folder_path: Optional[str] = None,
        cookies_id: Optional[str] = None,
        profile_path: Optional[str] = None,
    ) -> str:
        return cookies_folder_path or os.path.join(
            '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir(),
            Constants.GENERAL_COOKIES_FOLDER_NAME,
            cookies_id if cookies_id else profile_path.strip(os.sep).split(os.sep)[-1] if profile_path else Constants.DEFAULT_COOKIES_ID
        )

    @classmethod
    def user_agent_path(
        cls,
        cookies_folder_path: Optional[str] = None,
        cookies_id: Optional[str] = None,
        profile_path: Optional[str] = None
    ) -> str:
        return os.path.join(cls.cookies_folder_path, Constants.USER_AGENT_FILE_NAME)

    @staticmethod
    def user_agent(
        user_agent: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> Optional[str]:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read().strip()
        elif user_agent:
            user_agent = user_agent.strip()

            if file_path:
                with open(file_path, 'w') as f:
                    f.write(user_agent)

            return user_agent

        return None

    @staticmethod
    def proxy(
        proxy: Optional[Union[Proxy, str]] = None,

        # proxy - legacy (kept for convenience)
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> Optional[Proxy]:
        if not proxy:
            if not host and not port:
                return None

            proxy = Proxy(host=host, port=port)

        return proxy if isinstance(proxy, Proxy) else Proxy.from_str(proxy)


# -------------------------------------------------------------------------------------------------------------------------------- #