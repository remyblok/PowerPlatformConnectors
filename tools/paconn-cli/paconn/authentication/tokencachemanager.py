# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Token manager for Public Client Application.
"""

import os
import atexit
import pickle
import msal

from knack.util import CLIError
from knack.log import get_logger
from paconn.common.util import get_config_dir

LOGGER = get_logger(__name__)

_TOKEN_CACHE_FILE = 'token_cache.json'
_HTTP_CACHE_FILE = 'http_cache.bin'

class TokenCacheManager:
    """
    Class to manager token caches.
    """
    __token_cache = msal.SerializableTokenCache()
    __http_cache = {}

    __token_cache_deserialized = False
    __http_cache_deserialized = False

    @classmethod
    def get_http_cache(cls):
        http_cache_filepath = os.path.join(get_config_dir(), _HTTP_CACHE_FILE)
        LOGGER.debug("http cache file path {}".format(http_cache_filepath))

        if not cls.__http_cache_deserialized:
            # Setup HTTP Cache
            if os.path.exists(http_cache_filepath):
                try:
                    with open(http_cache_filepath, "rb") as f:
                        cls.__http_cache = pickle.load(f)  # Take a snapshot
                except (pickle.UnpicklingError): # A corrupted http cache file
                    cls.__http_cache = {}  # Recover by starting afresh
        
            # Saving back to file at exit
            atexit.register(lambda: pickle.dump(
                cls.__http_cache, open(http_cache_filepath, "wb")))
            cls.__http_cache_deserialized = True
            
        return cls.__http_cache


    @classmethod
    def get_token_cache(cls):
        token_cache_filepath = os.path.join(get_config_dir(), _TOKEN_CACHE_FILE)
        LOGGER.debug("token cache file path {}".format(token_cache_filepath))
        
        if not cls.__token_cache_deserialized:
            if os.path.exists(token_cache_filepath):
                with open(token_cache_filepath, "r", encoding="utf-8") as f:
                    cls.__token_cache.deserialize(f.read())

            atexit.register(lambda:
                open(token_cache_filepath, "w", encoding="utf-8")
                    .write(cls.__token_cache.serialize())
                    # Persists only when state changed
                    if cls.__token_cache.has_state_changed else None
            )
            cls.__token_cache_deserialized = True
                
        return cls.__token_cache


    @classmethod
    def clear_caches(cls):
        """
        Clear all cached authentication information
        """
        http_cache_filepath = os.path.join(get_config_dir(), _HTTP_CACHE_FILE)
        token_cache_filepath = os.path.join(get_config_dir(), _TOKEN_CACHE_FILE)

        if os.path.exists(http_cache_filepath):
            os.remove(http_cache_filepath)
        if os.path.exists(token_cache_filepath):
            os.remove(token_cache_filepath)
        
        cls.__http_cache.clear()
        cls.__token_cache = msal.SerializableTokenCache()


    @staticmethod
    def validate_token(token):
        if not token:
            raise CLIError('Access token invalid. Please login again.')
        elif "access_token" in token:
            return token
        elif "error" in token and "error_codes" in token and 7000216 in token["error_codes"]:
            raise CLIError('Need client secret and tenant to login. Please login again.')
        elif "error" in token:
            raise CLIError(token.get("error") + " " + token.get("error_description", ""))
        else:
            raise Exception('Please login again.')

            
