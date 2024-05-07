# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Validate command.
"""

from paconn import _VALIDATE

from paconn.common.util import display_message, display_error
from paconn.settings.util import load_powerapps_and_flow_rp
from paconn.settings.settingsbuilder import SettingsBuilder

import paconn.operations.validate


def validate(
        api_definition,
        powerapps_url,
        powerapps_version,
        settings_file,
        account):
    """
    Validate command.
    """
    # Get settings
    settings = SettingsBuilder.get_settings(
        environment=None,
        settings_file=settings_file,
        api_properties=None,
        api_definition=api_definition,
        icon=None,
        script=None,
        connector_id=None,
        powerapps_url=powerapps_url,
        powerapps_version=powerapps_version,
        account=account)

    powerapps_rp, _ = load_powerapps_and_flow_rp(
        settings=settings,
        command_context=_VALIDATE)

    result = paconn.operations.validate.validate(
        powerapps_rp=powerapps_rp,
        settings=settings)

    if result:
        display_error(result)
    else:
        display_message('{} validated successfully.'.format(settings.api_definition))
