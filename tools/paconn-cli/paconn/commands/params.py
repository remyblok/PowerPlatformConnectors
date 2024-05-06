# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
CLI parameter definitions
"""

from knack.arguments import ArgumentsContext
from paconn import _LOGIN, _DOWNLOAD, _CREATE, _UPDATE, _VALIDATE

OAUTH_SECRET = 'oauth_secret'
OAUTH_SECRET_OPTIONS = ['--secret', '-r']
OAUTH_SECRET_HELP = 'The OAuth2 client secret for the connector.'

ENVIRONMENT = 'environment'
ENVIRONMENT_OPTIONS = ['--env', '-e']
ENVIRONMENT_HELP = 'Power Platform environment ID.'

CONNECTOR_ID = 'connector_id'
CONNECTOR_ID_OPTIONS = ['--cid', '-c']
CONNECTOR_ID_HELP = 'The custom connector ID.'

POWERAPPS_URL = 'powerapps_url'
POWERAPPS_URL_OPTIONS = ['--pau', '-u']
POWERAPPS_URL_HELP = 'Power Platform URL.'

POWERAPPS_VERSION = 'powerapps_version'
POWERAPPS_VERSION_OPTIONS = ['--pav', '-v']
POWERAPPS_VERSION_HELP = 'Power Platform api version.'

SETTINGS = 'settings_file'
SETTINGS_OPTIONS = ['--settings', '-s']
SETTINGS_HELP = 'A settings file containing required parameters. When a settings file is specified some commandline parameters are ignored.'  # noqa: E501

API_PROPERTIES = 'api_properties'
API_PROPERTIES_OPTIONS = ['--api-prop', '-p']
API_PROPERTIES_HELP = 'Location of the API properties JSON document.'

API_DEFINITION = 'api_definition'
API_DEFINITION_OPTIONS = ['--api-def', '-d']
API_DEFINITION_HELP = 'Location of the Open API definition JSON document.'

ICON = 'icon'
ICON_OPTIONS = ['--icon', '-i']
ICON_HELP = 'Location for the icon file.'

SCRIPT = 'script'
SCRIPT_OPTIONS = ['--script', '-x']
SCRIPT_HELP = 'Location for the script file.'

ACCOUNT = 'account'
ACCOUNT_OPTIONS = ['--account', '-n']
ACCOUNT_HELP = 'Specific a logged in username or client id used during execution.'

# pylint: disable=unused-argument
def load_arguments(self, command):
    """
    Load command line arguments
    """
    with ArgumentsContext(self, _LOGIN) as arg_context:
        arg_context.argument(
            'client_id',
            options_list=['--client-id', '--clid', '-i'],
            type=str,
            required=False,
            help='ID of the application registered in Entra ID you want to use as Service Principal for login.')
        arg_context.argument(
            'client_secret',
            options_list=['--client-secret'],
            type=str,
            required=False,
            help='The client secret associated with the Client ID regsitered in Entra ID.')
        arg_context.argument(
            'tenant',
            options_list=['--tenant', '-t'],
            type=str,
            required=False,
            help='The tenant where the application specified by the Client ID is registered.')
        arg_context.argument(
            'authority_url',
            options_list=['--authority_url', '-a'],
            type=str,
            required=False,
            help='Authority URL for login.')
        arg_context.argument(
            'scopes',
            options_list=['--scopes', '-c'],
            type=str,
            required=False,
            help='Scopes for login.')
        arg_context.argument(
            'resource',
            options_list=['--resource', '-r'],
            type=str,
            required=False,
            help='Resource URL for login. Scope-argument will take precidence. Will be converted to /.default scope')
        arg_context.argument(
            SETTINGS,
            options_list=SETTINGS_OPTIONS,
            type=str,
            required=False,
            help=SETTINGS_HELP)
        arg_context.argument(
            'force',
            options_list=['--force', '-f'],
            type=bool,
            required=False,
            nargs='?',
            default=False,
            const=True,
            help='Override a previous login, if exists.')
        arg_context.argument(
            'username',
            options_list=['--username', '-n'],
            type=str,
            required=False,
            help='Username of the account you want to login to')
        arg_context.argument(
            'interactive',
            options_list=['--interactive', '-ui'],
            type=bool,
            required=False,
            nargs='?',
            default=False,
            const=True,
            help='Use Interactive login in stead of the default Device Code login.')
        arg_context.argument(
            'disable_broker_on_windows',
            options_list=['--disable-broker-on-windows', '-b'],
            type=bool,
            required=False,
            nargs='?',
            default=False,
            const=True,
            help='Disable the integration with Windows accounts on your device.')


    with ArgumentsContext(self, _DOWNLOAD) as arg_context:
        arg_context.argument(
            ENVIRONMENT,
            options_list=ENVIRONMENT_OPTIONS,
            type=str,
            required=False,
            help=ENVIRONMENT_HELP)
        arg_context.argument(
            CONNECTOR_ID,
            options_list=CONNECTOR_ID_OPTIONS,
            type=str,
            required=False,
            help=CONNECTOR_ID_HELP)
        arg_context.argument(
            'destination',
            options_list=['--dest', '-d'],
            type=str,
            required=False,
            help='Destination directory. Non-existent directories will be created.')
        arg_context.argument(
            POWERAPPS_URL,
            options_list=POWERAPPS_URL_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_URL_HELP)
        arg_context.argument(
            POWERAPPS_VERSION,
            options_list=POWERAPPS_VERSION_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_VERSION_HELP)
        arg_context.argument(
            SETTINGS,
            options_list=SETTINGS_OPTIONS,
            type=str,
            required=False,
            help=SETTINGS_HELP)
        arg_context.argument(
            'overwrite',
            options_list=['--overwrite', '-w'],
            type=bool,
            required=False,
            nargs='?',
            default=False,
            const=True,
            help='Overwrite all the existing connector and settings files.')
        arg_context.argument(
            ACCOUNT,
            options_list=ACCOUNT_OPTIONS,
            type=str,
            required=False,
            help=ACCOUNT_HELP)


    with ArgumentsContext(self, _CREATE) as arg_context:
        arg_context.argument(
            ENVIRONMENT,
            options_list=ENVIRONMENT_OPTIONS,
            type=str,
            required=False,
            help=ENVIRONMENT_HELP)
        arg_context.argument(
            API_PROPERTIES,
            options_list=API_PROPERTIES_OPTIONS,
            type=str,
            required=False,
            help=API_PROPERTIES_HELP)
        arg_context.argument(
            API_DEFINITION,
            options_list=API_DEFINITION_OPTIONS,
            type=str,
            required=False,
            help=API_DEFINITION_HELP)
        arg_context.argument(
            ICON,
            options_list=ICON_OPTIONS,
            type=str,
            required=False,
            help=ICON_HELP)
        arg_context.argument(
            SCRIPT,
            options_list=SCRIPT_OPTIONS,
            type=str,
            required=False,
            help=SCRIPT_HELP)
        arg_context.argument(
            POWERAPPS_URL,
            options_list=POWERAPPS_URL_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_URL_HELP)
        arg_context.argument(
            POWERAPPS_VERSION,
            options_list=POWERAPPS_VERSION_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_VERSION_HELP)
        arg_context.argument(
            OAUTH_SECRET,
            options_list=OAUTH_SECRET_OPTIONS,
            type=str,
            required=False,
            help=OAUTH_SECRET_HELP)
        arg_context.argument(
            SETTINGS,
            options_list=SETTINGS_OPTIONS,
            type=str,
            required=False,
            help=SETTINGS_HELP)
        arg_context.argument(
            'overwrite_settings',
            options_list=['--overwrite-settings', '-w'],
            type=bool,
            required=False,
            nargs='?',
            default=False,
            const=True,
            help='Overwrite the existing settings file.')
        arg_context.argument(
            ACCOUNT,
            options_list=ACCOUNT_OPTIONS,
            type=str,
            required=False,
            help=ACCOUNT_HELP)


    with ArgumentsContext(self, _UPDATE) as arg_context:
        arg_context.argument(
            ENVIRONMENT,
            options_list=ENVIRONMENT_OPTIONS,
            type=str,
            required=False,
            help=ENVIRONMENT_HELP)
        arg_context.argument(
            API_PROPERTIES,
            options_list=API_PROPERTIES_OPTIONS,
            type=str,
            required=False,
            help=API_PROPERTIES_HELP)
        arg_context.argument(
            API_DEFINITION,
            options_list=API_DEFINITION_OPTIONS,
            type=str,
            required=False,
            help=API_DEFINITION_HELP)
        arg_context.argument(
            ICON,
            options_list=ICON_OPTIONS,
            type=str,
            required=False,
            help=ICON_HELP)
        arg_context.argument(
            SCRIPT,
            options_list=SCRIPT_OPTIONS,
            type=str,
            required=False,
            help=SCRIPT_HELP)
        arg_context.argument(
            CONNECTOR_ID,
            options_list=CONNECTOR_ID_OPTIONS,
            type=str,
            required=False,
            help=CONNECTOR_ID_HELP)
        arg_context.argument(
            POWERAPPS_URL,
            options_list=POWERAPPS_URL_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_URL_HELP)
        arg_context.argument(
            POWERAPPS_VERSION,
            options_list=POWERAPPS_VERSION_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_VERSION_HELP)
        arg_context.argument(
            OAUTH_SECRET,
            options_list=OAUTH_SECRET_OPTIONS,
            type=str,
            required=False,
            help=OAUTH_SECRET_HELP)
        arg_context.argument(
            SETTINGS,
            options_list=SETTINGS_OPTIONS,
            type=str,
            required=False,
            help=SETTINGS_HELP)
        arg_context.argument(
            ACCOUNT,
            options_list=ACCOUNT_OPTIONS,
            type=str,
            required=False,
            help=ACCOUNT_HELP)


    with ArgumentsContext(self, _VALIDATE) as arg_context:
        arg_context.argument(
            API_DEFINITION,
            options_list=API_DEFINITION_OPTIONS,
            type=str,
            required=False,
            help=API_DEFINITION_HELP)
        arg_context.argument(
            POWERAPPS_URL,
            options_list=POWERAPPS_URL_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_URL_HELP)
        arg_context.argument(
            POWERAPPS_VERSION,
            options_list=POWERAPPS_VERSION_OPTIONS,
            type=str,
            required=False,
            help=POWERAPPS_VERSION_HELP)
        arg_context.argument(
            SETTINGS,
            options_list=SETTINGS_OPTIONS,
            type=str,
            required=False,
            help=SETTINGS_HELP)
        arg_context.argument(
            ACCOUNT,
            options_list=ACCOUNT_OPTIONS,
            type=str,
            required=False,
            help=ACCOUNT_HELP)

