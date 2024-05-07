# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Utility for loading settings.
"""

import uuid
from knack.util import CLIError
from paconn import _UPDATE, _DOWNLOAD, _VALIDATE
from paconn.common.util import display_message, write_with_prompt
from paconn.authentication.publictokenmanager import PublicTokenManager
from paconn.authentication.confidentialtokenmanager import ConfidentialTokenManager
from paconn.authentication.auth import _USERNAME, _CLIENT_ID
from paconn.apimanager.powerappsrpbuilder import PowerAppsRPBuilder
from paconn.apimanager.flowrpbuilder import FlowRPBuilder
from paconn.common.prompts import get_environment, get_connector_id, get_account
from paconn.settings.settingsserializer import SettingsSerializer

# Setting file name
SETTINGS_FILE = 'settings.json'


def prompt_for_environment(settings, flow_rp):
    # Select environment if not provided
    if not hasattr(settings, 'environment') or not settings.environment:
        settings.environment = get_environment(
            flow_rp=flow_rp)


def prompt_for_connector_id(settings, powerapps_rp):
    # Select connector id if not provided
    if (not hasattr(settings, 'connector_id') or not settings.connector_id):
        settings.connector_id = get_connector_id(
            powerapps_rp=powerapps_rp,
            environment=settings.environment)

def load_powerapps_and_flow_rp(settings, command_context):

    # Get credentials
    credentials = get_credentials(settings)

    # Get powerapps rp
    powerapps_rp = PowerAppsRPBuilder.get_from_settings(
        credentials=credentials,
        settings=settings)

    # Get flow rp
    flow_rp = FlowRPBuilder.get_from_settings(
        credentials=credentials,
        settings=settings)

    # If the file names are missing for the download command
    # use default names
    if command_context is _DOWNLOAD:
        settings.api_properties = settings.api_properties or 'apiProperties.json'
        settings.api_definition = settings.api_definition or 'apiDefinition.swagger.json'
        settings.icon = settings.icon or 'icon.png'
        settings.script = settings.script or 'script.csx'

    # Prompt for environment for any
    # operation other than `validate`
    if command_context is not _VALIDATE:
        prompt_for_environment(
            settings=settings,
            flow_rp=flow_rp)

    # Prompt for connector id for
    # operation `update` and `download`
    if command_context is _UPDATE or command_context is _DOWNLOAD:
        prompt_for_connector_id(
            settings=settings,
            powerapps_rp=powerapps_rp)

    return powerapps_rp, flow_rp

def write_settings(settings, overwrite):
    filename = SETTINGS_FILE
    settings_json = SettingsSerializer.to_json_string(settings)
    write_with_prompt(
        filename=filename,
        mode='w',
        content=settings_json,
        overwrite=overwrite)

def get_credentials(settings):
    manager = None
    
    if not settings.account:
        select_account(settings)

    if is_valid_uuid(settings.account):
        manager = ConfidentialTokenManager(settings)
    else:
        manager = PublicTokenManager(settings)

    
    credentials = manager.get_token()
    return credentials


def select_account(settings):
    manager = PublicTokenManager(settings)
    accounts = manager.list_accounts()

    apps = ConfidentialTokenManager.list_apps()

    if not accounts and not apps:
        raise CLIError('No logged in accounts. Please login first')
    if len(accounts) == 1 and not apps:
        settings.account = accounts[0][_USERNAME]
        display_message("Logged in as user {}".format(settings.account), flush=True)
    elif not accounts and len(apps) == 1:
        settings.account = apps[0][_CLIENT_ID]
        display_message("Logged in as app {}".format(settings.account), flush=True)
    else:    
        settings.account = get_account(accounts, apps)


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False