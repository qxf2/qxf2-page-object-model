"""This modules contains interfaces for communications with GA.

Copyright (c) 2020 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from pkg_resources import get_distribution
import requests
from uuid import uuid4

from .constants import GA_INSTANCE, GA_ENDPOINT

logger = logging.getLogger(__name__)


def _get_client_info():
    """Get name of the client and its version.

    :return: ('reportportal-client', '5.0.4')
    """
    client = get_distribution('reportportal-client')
    return client.project_name, client.version


def send_event(agent_name, agent_version):
    """Send an event to GA about client and agent versions with their names.

    :param agent_name:    Name of the agent that uses the client
    :param agent_version: Version of the agent
    """
    client_name, client_version = _get_client_info()
    payload = {
        'v': '1',
        'tid': GA_INSTANCE,
        'aip': '1',
        'cid': str(uuid4()),
        't': 'event',
        'ec': 'Client name "{}", version "{}"'.format(
            client_name, client_version
        ),
        'ea': 'Start launch',
        'el': 'Agent name "{}", version "{}"'.format(
            agent_name, agent_version
        )
    }
    headers = {'User-Agent': 'Universal Analytics'}
    try:
        return requests.post(url=GA_ENDPOINT, data=payload, headers=headers)
    except requests.exceptions.RequestException as err:
        logger.debug('Failed to send data to Google Analytics: %s',
                     str(err))
