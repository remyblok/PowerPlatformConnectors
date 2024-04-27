# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Token file manager.
"""

import os
import atexit
import pickle
import msal

from knack.util import CLIError
from paconn.common.util import display_message, get_config_dir

_TOKEN_CACHE_FILE = 'token_cache.json'
_HTTP_CACHE_FILE = 'http_cache.bin'

# Token specific variables
_TOKEN_TYPE = 'token_type'
_ACCESS_TOKEN = 'access_token'
_EXPIRES_ON = 'expires_on'
_OID = 'oid'
_USERNAME = "username"

class TokenManager:
    """
    Class to manager login token.
    """
    __singleton_client = None
    __http_cache = {}

    def __init__(self, settings):
        self.__settings = settings
        self.__client = TokenManager.__initialize_msal_application(settings)

    @classmethod
    def __initialize_msal_application(cls, settings,
            token_cache_file=_TOKEN_CACHE_FILE,
            http_cache_file=_HTTP_CACHE_FILE):
        """
        Initialize the MSAL application so it functions as singleton
        """
        if cls.__singleton_client:
            return cls.__singleton_client

        http_cache_filepath = os.path.join(get_config_dir(), http_cache_file)
        token_cache_filepath = os.path.join(get_config_dir(), token_cache_file)

        cls.__http_cache = {}
        if os.path.exists(http_cache_filepath):
            try:
                with open(http_cache_filepath, "rb") as f:
                    cls.__http_cache = pickle.load(f)  # Take a snapshot
            except (
                    FileNotFoundError,
                    pickle.UnpicklingError, # A corrupted http cache file
                ):
                cls.__http_cache = {}  # Recover by starting afresh
        # When exit, write http cache back to the file.
        atexit.register(lambda: pickle.dump(
            cls.__http_cache, open(http_cache_filepath, "wb")))

        token_cache = msal.SerializableTokenCache()
        if os.path.exists(token_cache_filepath):
            with open(token_cache_filepath, "r", encoding="utf-8") as f:
                token_cache.deserialize(f.read())
        # When exit, write token cache back to the file.
        atexit.register(lambda:
            open(token_cache_filepath, "w", encoding="utf-8")
                .write(token_cache.serialize())
            # Persists only when state changed
            if token_cache.has_state_changed else None
        )

        client = msal.PublicClientApplication(
                    settings.client_id,
                    authority=settings.authority_url,
                    enable_broker_on_windows= not settings.disable_broker_on_windows,
                    token_cache=token_cache,
                    http_cache=cls.__http_cache)
        cls.__singleton_client = client
        return client

    @classmethod
    def clear_caches(cls, token_cache_file=_TOKEN_CACHE_FILE, http_cache_file=_HTTP_CACHE_FILE):
        """
        Clear all cached authentication information
        """
        http_cache_filepath = os.path.join(get_config_dir(), http_cache_file)
        token_cache_filepath = os.path.join(get_config_dir(), token_cache_file)

        if os.path.exists(http_cache_filepath):
            os.remove(http_cache_filepath)
        if os.path.exists(token_cache_filepath):
            os.remove(token_cache_filepath)
        cls.__http_cache.clear()

    
    def list_accounts(self):
        accounts = self.__client.get_accounts()
        return accounts


    def get_token(self):
        """
        Returns a valid token when available, or exception.
        """
        token = self.__authenticate_cached()
        return self.__validate_token(token)


    def is_authenticated(self):
        """
        returns if a valid token is available
        """
        accounts = self.__client.get_accounts(self.__settings.username)
        if not accounts:
            return False
        
        token = self.__client.acquire_token_silent(self.__settings.scopes, accounts[0])
        return token is not None


    def authenticate_with_device_code(self):
        """
        Authenticate the end-user using device auth.
        """
        flow = self.__client.initiate_device_flow(self.__settings.scopes)

        display_message(flow['message'], flush=True)

        token = self.__client.acquire_token_by_device_flow(flow)
        return self.__validate_token(token)


    def authenticate_interactive(self):
        """
        Authenticate the end-user using interactive mode.
        """
        token = self.__client.acquire_token_interactive(
            self.__settings.scopes,
            domain_hint=self.__settings.tenant,
            login_hint=self.__settings.username,
            parent_window_handle=self.__client.CONSOLE_WINDOW_HANDLE)
        return self.__validate_token(token)


    def __authenticate_cached(self):
        """
        Returns a valid token when available.
        """

        if not self.__settings.username:
            raise Exception('Expected username setting to be provided')

        accounts = self.__client.get_accounts(self.__settings.username)
        if not accounts:
            raise CLIError('Unknown account {}. Please login again.'.format(self.__settings.username))

        token = self.__client.acquire_token_silent(self.__settings.scopes, accounts[0])
        return token 


    def __validate_token(self, token):
        if not token:
            raise CLIError('Access token invalid. Please login again.')
        elif "access_token" in token:
            return token
        elif "error" in token:
            raise CLIError (token.get("error"))
        else:
            raise Exception('Please login again.')

            
