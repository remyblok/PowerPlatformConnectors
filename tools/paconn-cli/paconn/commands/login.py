# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Login command.
"""

from paconn.authentication.auth import get_authentication
from paconn.common.util import display_message
from paconn.settings.settingsbuilder import SettingsBuilder


def login(client_id, tenant, authority_url, resource, scopes, settings_file, force):
    """
    Login command.
    """
    # Get settings
    settings = SettingsBuilder.get_authentication_settings(
        settings_file=settings_file,
        client_id=client_id,
        tenant=tenant,
        authority_url=authority_url,
        resource=resource,
        scopes=scopes)

    get_authentication(
        settings=settings,
        force_authenticate=force)
    display_message('Login successful.')
