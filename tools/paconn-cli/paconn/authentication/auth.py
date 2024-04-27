# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
Authentication methods
"""

from paconn.authentication.tokenmanager import TokenManager

def get_authentication(settings, force_authenticate):
    """
    Logs the user in based on the specified settings
    """
    tokenmanager = TokenManager(settings)

    if not force_authenticate:
        token = tokenmanager.is_authenticated()

    if not token:
        if settings.interactive_login:
            token = tokenmanager.authenticate_interactive()
        else:
            token = tokenmanager.authenticate_with_device_code()



def remove_authentication():
    """
    Removes any cached authentication
    """
    TokenManager.clear_caches()
