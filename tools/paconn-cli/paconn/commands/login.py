# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Login command.
"""

from paconn.authentication.auth import get_user_authentication, get_app_authentication
from paconn.common.util import display_message
from paconn.settings.settingsbuilder import SettingsBuilder


def login(client_id, client_secret, tenant, authority_url, resource, scopes, settings_file, force, 
          username, interactive, disable_broker_on_windows):
    """
    Login command.
    """
    # Get settings
    settings = SettingsBuilder.get_authentication_settings(
        settings_file=settings_file,
        client_id=client_id,
        client_secret=client_secret,
        tenant=tenant,
        authority_url=authority_url,
        resource=resource,
        scopes=scopes,
        username=username,
        interactive_login=interactive,
        disable_broker_on_windows=disable_broker_on_windows)

    if client_secret:
        get_app_authentication(settings)
        display_message('Login successful for application {}.'.format(settings.client_id))
    else:
        accounts = get_user_authentication(
            settings=settings,
            force_authenticate=force)
        display_message('Login successful. Known accounts:')
        for a in accounts:
            display_message('- {}'.format(a.get('username')))
        

    
