# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Token file manager.
"""

from knack import query
import msal

from knack.log import get_logger
from paconn.authentication.tokenmanagerbase import TokenManagerBase

LOGGER = get_logger(__name__)

_TOKEN_CACHE_FILE = 'confidential_token_cache.json'
_HTTP_CACHE_FILE = 'confidential_http_cache.bin'

class ConfidentialTokenManager(TokenManagerBase):
    """
    Class to manager login token.
    """

    def __init__(self, settings):
        self.__settings = settings
        self.__client = super()._initialize_msal_application(
            _TOKEN_CACHE_FILE,
            _HTTP_CACHE_FILE,
            lambda token_cache, http_cache : msal.ConfidentialClientApplication(
                    client_id=settings.client_id or settings.account,
                    client_credential=settings.client_secret,
                    authority=settings.authority_url,
                    token_cache=token_cache,
                    http_cache=http_cache
            )
        )

    @classmethod
    def clear_caches(cls):
        """
        Clear all cached authentication information
        """
        TokenManagerBase._clear_caches(_TOKEN_CACHE_FILE, _HTTP_CACHE_FILE)


    def get_token(self):
        """
        Returns a valid token when available, or exception.
        """
        token = self.__client.acquire_token_for_client(self.__settings.scopes)
        return super()._validate_token(token)


    def authenticate_application(self):
        """
        Authenticate using application secrets.
        """
        self.get_token()
        
        # Bit of a hack to make sure that the credentials are found when no '--tenant' is supplied
        cached_token = self.__client.token_cache.find(
            msal.TokenCache.CredentialType.ACCESS_TOKEN,
            target=self.__settings.scopes,
            query={ "client_id": self.__settings.client_id }
        )[0]
        cached_token['realm'] = "common";


