# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""
User profile management class.`
"""
import msal
from urllib.parse import urljoin
# AADTokenCredentials for multi-factor authentication
from msrestazure.azure_active_directory import AADTokenCredentials
from paconn.common.util import display_message


class Profile:
    """
    A Class representing user profile.
    """

    def __init__(self, client_id, tenant, scopes, authority_url):
        self.client_id = client_id
        self.tenant = tenant
        self.scopes = scopes.split()
        self.authority_url = authority_url

    def _get_authentication_context(self):
        auth_url = urljoin(self.authority_url, self.tenant)

        return msal.PublicClientApplication(
            self.client_id,
            authority=auth_url)

    def authenticate_device_code(self):
        """
        Authenticate the end-user using device auth.
        """
        context = self._get_authentication_context()

        flow = context.initiate_device_flow(
            scopes=self.scopes)

        display_message(code['message'], flush=True)

        mgmt_token = context.acquire_token_by_device_flow(flow)

        credentials = AADTokenCredentials(
            token=mgmt_token,
            client_id=self.client_id)

        return credentials.token
