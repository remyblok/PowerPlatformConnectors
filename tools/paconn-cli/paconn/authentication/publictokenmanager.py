# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Token manager for Public Client Application.
"""

import msal

from knack.util import CLIError
from knack.log import get_logger
from paconn.authentication.tokencachemanager import TokenCacheManager
from paconn.common.util import display_message

LOGGER = get_logger(__name__)

class PublicTokenManager:
    """
    Class to manager login token.
    """

    def __init__(self, settings):
        self.__settings = settings
        self.__client = msal.PublicClientApplication(
                    settings.client_id,
                    authority=settings.authority_url,
                    enable_broker_on_windows=not settings.disable_broker_on_windows,
                    token_cache=TokenCacheManager.get_token_cache(),
                    http_cache=TokenCacheManager.get_http_cache())

    
    def list_accounts(self):
        """
        Get a list of all logged in accounts
        """
        accounts = self.__client.get_accounts()
        return accounts


    def get_token(self):
        """
        Returns a valid token when available, or exception.
        """
        token = self.__authenticate_cached()
        return TokenCacheManager.validate_token(token)


    def is_authenticated(self):
        """
        Returns if any valid token is available
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
        TokenCacheManager.validate_token(token)


    def authenticate_interactive(self):
        """
        Authenticate the end-user using interactive mode.
        """
        token = self.__client.acquire_token_interactive(
            self.__settings.scopes,
            domain_hint=self.__settings.tenant,
            login_hint=self.__settings.username,
            parent_window_handle=self.__client.CONSOLE_WINDOW_HANDLE)
        TokenCacheManager.validate_token(token)


    def __authenticate_cached(self):
        """
        Returns a valid token when available.
        """
        if not self.__settings.account:
            raise Exception('Expected account setting to be provided')

        LOGGER.debug("Acquire token silent for {}".format(self.__settings.account))
        
        accounts = self.__client.get_accounts(self.__settings.account)
        if not accounts:
            raise CLIError('Unknown account {}. Please login again.'.format(self.__settings.account))

        token = self.__client.acquire_token_silent(self.__settings.scopes, accounts[0])
        return token 
