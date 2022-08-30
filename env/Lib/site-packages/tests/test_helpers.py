"""This modules contains unit tests for the helpers module."""

from six.moves import mock

from reportportal_client.helpers import (
    gen_attributes,
    get_launch_sys_attrs,
    get_package_version,
    verify_value_length
)


def test_gen_attributes():
    """Test functionality of the gen_attributes function."""
    expected_out = [{'value': 'Tag'}, {'key': 'Key', 'value': 'Value'}]
    out = gen_attributes(['Tag', 'Key:Value', ''])
    assert expected_out == out


@mock.patch('reportportal_client.helpers.system',
            mock.Mock(return_value='linux'))
@mock.patch('reportportal_client.helpers.machine',
            mock.Mock(return_value='Windows-PC'))
@mock.patch('reportportal_client.helpers.processor',
            mock.Mock(return_value='amd'))
def test_get_launch_sys_attrs():
    """Test for validate get_launch_sys_attrs function."""
    expected_result = {'cpu': 'amd',
                       'machine': 'Windows-PC',
                       'os': 'linux',
                       'system': True}
    assert get_launch_sys_attrs() == expected_result


@mock.patch('reportportal_client.helpers.system', mock.Mock())
@mock.patch('reportportal_client.helpers.machine', mock.Mock())
@mock.patch('reportportal_client.helpers.processor',
            mock.Mock(return_value=''))
def test_get_launch_sys_attrs_docker():
    """Test that cpu key value is not empty.

    platform.processor() returns empty string in case it was called
    inside of the Docker container. API does not allow empty values
    for the attributes.
    """
    result = get_launch_sys_attrs()
    assert result['cpu'] == 'unknown'


def test_get_package_version():
    """Test for the get_package_version() function-helper."""
    assert get_package_version('noname') == 'not found'


def test_verify_value_length():
    """Test for validate verify_value_length() function."""
    inputl = [{'key': 'tn', 'value': 'v' * 130}, [1, 2],
              {'value': 'tv2'}, {'value': 300}]
    expected = [{'key': 'tn', 'value': 'v' * 128}, [1, 2],
                {'value': 'tv2'}, {'value': 300}]
    assert verify_value_length(inputl) == expected
