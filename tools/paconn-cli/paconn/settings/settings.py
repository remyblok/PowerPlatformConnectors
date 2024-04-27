# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
"""
Represents a settings object constructed from settings.json
"""


# pylint: disable=too-few-public-methods
class Settings:
    """
    Represents a settings object constructed from settings.json
    """
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            connector_id,
            environment,
            api_properties,
            api_definition,
            icon,
            script,
            powerapps_url,
            powerapps_api_version,
            flow_url=None,
            flow_api_version=None,
            client_id=None,
            tenant=None,
            authority_url=None,
            resource=None,
            scopes=None,
            username=None,
            interactive_login=False,
            disable_broker_on_windows=False):

        # connector specific settings
        self.connector_id = connector_id
        self.environment = environment

        # Files
        self.api_properties = api_properties
        self.api_definition = api_definition
        self.icon = icon
        self.script = script

        # PowerApps RP settings
        self.powerapps_url = powerapps_url or 'https://api.powerapps.com'
        self.powerapps_api_version = powerapps_api_version or '2016-11-01'
        self.powerapps_base_path = 'providers/Microsoft.PowerApps'         # Constant

        # Flow RP Settings
        self.flow_url = flow_url or 'https://api.flow.microsoft.com'
        self.flow_api_version = flow_api_version or '2016-11-01'
        self.flow_base_path = 'providers/Microsoft.ProcessSimple'          # Constant

        self.client_id = client_id or '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
        self.tenant = tenant or 'common'
        self.authority_url = authority_url or 'https://login.microsoftonline.com/' + self.tenant
        
        if scopes:
            self.scopes = scopes.split()
        elif resource: 
            self.scopes = [resource + "/.default"]
        else:
            self.scopes = ['https://service.powerapps.com/.default']
            
        self.username = username
        self.interactive_login = interactive_login
        self.disable_broker_on_windows = disable_broker_on_windows
