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

class TokenManagerBase:
    """
    Class to manager login token.
    """
    __singleton_client = None
    __http_cache = {}

    @classmethod
    def _initialize_msal_application(cls, token_cache_file, http_cache_file, create_client):
        """
        Initialize the MSAL application so it functions as singleton
        """
        if cls.__singleton_client:
            LOGGER.debug("Reuse singleton msal application")
            return cls.__singleton_client

        LOGGER.debug("Create msal application")
        
        #setup cache file locations
        http_cache_filepath = os.path.join(get_config_dir(), http_cache_file)
        token_cache_filepath = os.path.join(get_config_dir(), token_cache_file)
        LOGGER.debug("http cache file path {}".format(http_cache_filepath))
        LOGGER.debug("token cache file path {}".format(token_cache_filepath))

        # Setup HTTP Cache + saving at exit
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
        atexit.register(lambda: pickle.dump(
            cls.__http_cache, open(http_cache_filepath, "wb")))

        # Setup Token Cache + saving at exit
        token_cache = msal.SerializableTokenCache()
        if os.path.exists(token_cache_filepath):
            with open(token_cache_filepath, "r", encoding="utf-8") as f:
                token_cache.deserialize(f.read())
        atexit.register(lambda:
            open(token_cache_filepath, "w", encoding="utf-8")
                .write(token_cache.serialize())
            # Persists only when state changed
            if token_cache.has_state_changed else None
        )
        
        cls.__singleton_client = create_client(token_cache, cls.__http_cache)
        return cls.__singleton_client
    
    @classmethod
    def _clear_caches(cls, token_cache_file, http_cache_file):
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

    
    def _validate_token(self, token):
        if not token:
            raise CLIError('Access token invalid. Please login again.')
        elif "access_token" in token:
            return token
        elif "error" in token and "error_codes" in token and 7000216 in token["error_codes"]:
            raise CLIError('Need client secret and tenant to login. Please login again.')
        elif "error" in token:
            raise CLIError (token.get("error") + " " + token.get("error_description", ""))
        else:
            raise Exception('Please login again.')

            
