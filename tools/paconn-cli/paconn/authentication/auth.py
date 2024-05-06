# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Authentication methods
"""

from paconn.authentication.publictokenmanager import PublicTokenManager
from paconn.authentication.confidentialtokenmanager import ConfidentialTokenManager

# Token specific variables
_TOKEN_TYPE = 'token_type'
_ACCESS_TOKEN = 'access_token'
_EXPIRES_ON = 'expires_on'
_OID = 'oid'
_USERNAME = "username"

def get_user_authentication(settings, force_authenticate):
    """
    Logs the user in based on the specified settings
    """
    tokenmanager = PublicTokenManager(settings)
    hasToken = False

    if not force_authenticate:
        hasToken = tokenmanager.is_authenticated()

    if not hasToken:
        if settings.interactive_login:
            tokenmanager.authenticate_interactive()
        else:
            tokenmanager.authenticate_with_device_code()

    return tokenmanager.list_accounts()

def get_app_authentication(settings):
    """
    Login using app credentials
    """
    tokenmanager = ConfidentialTokenManager(settings)
    tokenmanager.authenticate_application()


def remove_authentication():
    """
    Removes any cached authentication
    """
    PublicTokenManager.clear_caches()
    ConfidentialTokenManager.clear_caches()
