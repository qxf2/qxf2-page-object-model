"""This module contains unit tests for analytics used in the project.

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

from requests.exceptions import RequestException

from six.moves import mock

from reportportal_client.external.constants import GA_ENDPOINT, GA_INSTANCE
from reportportal_client.external.google_analytics import send_event


@mock.patch('reportportal_client.external.google_analytics.uuid4',
            mock.Mock(return_value=555))
@mock.patch('reportportal_client.external.google_analytics.requests.post')
@mock.patch('reportportal_client.external.google_analytics.get_distribution')
def test_send_event(mocked_distribution, mocked_requests):
    """Test functionality of the send_event() function.

    :param mocked_distribution: Mocked get_distribution() function
    :param mocked_requests:     Mocked requests module
    """
    expected_cl_version, expected_cl_name = '5.0.4', 'reportportal-client'
    agent_version, agent_name = '5.0.5', 'pytest-reportportal'
    mocked_distribution.return_value.version = expected_cl_version
    mocked_distribution.return_value.project_name = expected_cl_name

    expected_headers = {'User-Agent': 'Universal Analytics'}

    expected_data = {
        'v': '1',
        'tid': GA_INSTANCE,
        'aip': '1',
        'cid': '555',
        't': 'event',
        'ec': 'Client name "{}", version "{}"'.format(
            expected_cl_name, expected_cl_version
        ),
        'ea': 'Start launch',
        'el': 'Agent name "{}", version "{}"'.format(
            agent_name, agent_version
        )
    }
    send_event(agent_name, agent_version)
    mocked_requests.assert_called_with(
        url=GA_ENDPOINT, data=expected_data, headers=expected_headers)


@mock.patch('reportportal_client.external.google_analytics.uuid4',
            mock.Mock(return_value=555))
@mock.patch('reportportal_client.external.google_analytics.requests.post',
            mock.Mock(side_effect=RequestException))
@mock.patch('reportportal_client.external.google_analytics.get_distribution',
            mock.Mock())
def test_send_event_raises():
    """Test that the send_event() does not raise exceptions."""
    send_event('pytest-reportportal', '5.0.5')
