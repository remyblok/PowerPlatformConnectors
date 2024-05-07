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
from paconn.authentication.tokencachemanager import TokenCacheManager

LOGGER = get_logger(__name__)

class ConfidentialTokenManager:
    """
    Class to manager login token.
    """

    def __init__(self, settings):
        self.__settings = settings
        self.__client = msal.ConfidentialClientApplication(
                    client_id=settings.account or settings.client_id,
                    client_credential=settings.client_secret,
                    authority=settings.authority_url,
                    token_cache=TokenCacheManager.get_token_cache(),
                    http_cache=TokenCacheManager.get_http_cache())


    @classmethod
    def list_apps(cls):
        token_cache = TokenCacheManager.get_token_cache()

        tokens = token_cache.find(msal.TokenCache.CredentialType.ACCESS_TOKEN, query={
                'realm': "common"
            })
        tokens = filter(lambda t: t.get('home_account_id', None) is None, tokens)
        return list(tokens)
    

    def get_token(self):
        """
        Returns a valid token when available, or exception.
        """
        token = self.__client.acquire_token_for_client(self.__settings.scopes)
        return TokenCacheManager.validate_token(token)


    def authenticate_application(self):
        """
        Authenticate using application secrets.
        """
        self.get_token()
        
        # Bit of a hack to make sure that the credentials are found when no '--tenant' is supplied
        cache = self.__client.token_cache
        cached_token = cache.find(
            msal.TokenCache.CredentialType.ACCESS_TOKEN,
            target=self.__settings.scopes,
            query={ "client_id": self.__client.client_id }
        )[0]
        
        cached_token = cached_token.copy()
        cached_token['realm'] = "common";
        cache.modify(msal.TokenCache.CredentialType.ACCESS_TOKEN, cached_token, cached_token)
        
        


