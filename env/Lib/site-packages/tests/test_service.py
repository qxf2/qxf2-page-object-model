"""This modules includes unit tests for the service.py module."""

from datetime import datetime

from delayed_assert import assert_expectations, expect
import pytest
from six.moves import mock

from reportportal_client.service import (
    _convert_string,
    _dict_to_payload,
    _get_data,
    _get_id,
    _get_json,
    _get_messages,
    _get_msg
)


class TestServiceFunctions:
    """This class contains test methods for helper functions."""

    def test_check_convert_to_string(self):
        """Test for support and convert strings to utf-8."""
        expect(_convert_string('Hello world') == 'Hello world')
        expect(lambda: isinstance(_convert_string('Hello world'), str))
        assert_expectations()

    @pytest.mark.parametrize('system', [True, False])
    def test_dict_to_payload_with_system_key(self, system):
        """Test convert dict to list of dicts with key system."""
        initial_dict = {'aa': 1, 'b': 2, 'system': system}
        expected_list = [{'key': 'aa', 'value': '1', 'system': system},
                         {'key': 'b', 'value': '2', 'system': system}]
        assert _dict_to_payload(initial_dict) == expected_list

    def test_get_id(self, response):
        """Test for the get_id function."""
        assert _get_id(response(200, {'id': 123})) == 123

    def test_get_msg(self, response):
        """Test for the get_msg function."""
        fake_json = {'id': 123}
        assert _get_msg(response(200, fake_json)) == fake_json

    def test_get_data(self, response):
        """Test for the get_data function."""
        fake_json = {'id': 123}
        assert _get_data(response(200, fake_json)) == fake_json

    def test_get_json(self, response):
        """Test for the get_json function."""
        fake_json = {'id': 123}
        assert _get_json(response(200, fake_json)) == fake_json

    def test_get_messages(self):
        """Test for the get_messages function."""
        data = {'responses': [{'errorCode': 422, 'message': 'error'}]}
        assert _get_messages(data) == ['422: error']


class TestReportPortalService:
    """This class stores methods which test ReportPortalService."""

    @mock.patch('reportportal_client.service._get_data')
    def test_start_launch(self, mock_get, rp_service):
        """Test start launch and sending request.

        :param mock_get:   Mocked _get_data() function
        :param rp_service: Pytest fixture
        """
        mock_get.return_value = {'id': 111}
        launch_id = rp_service.start_launch('name', datetime.now().isoformat())
        assert launch_id == 111

    @mock.patch('reportportal_client.service._get_data')
    def test_start_launch_with_rerun(self, mock_get, rp_service):
        """Test start launch and sending request.

        :param mock_get:   Mocked _get_data() function
        :param rp_service: Pytest fixture
        """
        mock_get.return_value = {'id': 111}
        launch_id = rp_service.start_launch('name', datetime.now().isoformat(),
                                            rerun=True, rerunOf="111")
        assert launch_id == 111

    @mock.patch('reportportal_client.service._get_msg')
    def test_finish_launch(self, mock_get, rp_service):
        """Test finish launch and sending request.

        :param mock_get:   Mocked _get_msg() function
        :param rp_service: Pytest fixture
        """
        mock_get.return_value = {'id': 111}
        _get_msg = rp_service.finish_launch(
            'name', datetime.now().isoformat())
        assert _get_msg == {'id': 111}

    @mock.patch('reportportal_client.service._get_json',
                mock.Mock(return_value={'id': 112}))
    def test_get_launch_info(self, rp_service, monkeypatch):
        """Test get current launch information.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_resp = mock.Mock()
        mock_resp.status_code = 200

        mock_get = mock.Mock(return_value=mock_resp)
        monkeypatch.setattr(rp_service.session, 'get', mock_get)
        monkeypatch.setattr(rp_service, 'launch_id', '1234-cafe')

        launch_id = rp_service.get_launch_info()
        mock_get.assert_called_once_with(
            url='{0}/launch/uuid/{1}'.format(rp_service.base_url_v1,
                                             rp_service.launch_id),
            verify=rp_service.verify_ssl)
        assert launch_id == {'id': 112}

    def test_get_launch_info_launch_id_none(self, rp_service, monkeypatch):
        """Test get launch information for a non started launch.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_get = mock.Mock()
        monkeypatch.setattr(rp_service.session, 'get', mock_get)
        monkeypatch.setattr(rp_service, 'launch_id', None)

        launch_info = rp_service.get_launch_info()
        mock_get.assert_not_called()
        assert launch_info == {}

    @mock.patch('reportportal_client.service.sleep', mock.Mock())
    @mock.patch('reportportal_client.service._get_json',
                mock.Mock(return_value={"errorCode": 4041}))
    def test_get_launch_info_wrong_launch_id(self, rp_service, monkeypatch):
        """Test get launch information for a non existed launch.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_get = mock.Mock()
        monkeypatch.setattr(rp_service.session, 'get', mock_get)
        monkeypatch.setattr(rp_service, 'launch_id', '1234')

        launch_info = rp_service.get_launch_info()
        expect(mock_get.call_count == 5)
        expect(launch_info == {})
        assert_expectations()

    @mock.patch('reportportal_client.service.sleep', mock.Mock())
    @mock.patch('reportportal_client.service._get_json',
                mock.Mock(return_value={'id': 112}))
    def test_get_launch_info_1st_failed(self, rp_service, monkeypatch):
        """Test get launch information with 1st attempt failed.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_resp1 = mock.Mock()
        mock_resp1.status_code = 404
        mock_resp2 = mock.Mock()
        mock_resp2.status_code = 200
        mock_get = mock.Mock()
        mock_get.side_effect = [mock_resp1, mock_resp2]
        monkeypatch.setattr(rp_service.session, 'get', mock_get)
        monkeypatch.setattr(rp_service, 'launch_id', '1234')

        launch_info = rp_service.get_launch_info()
        expect(mock_get.call_count == 2)
        expect(launch_info == {'id': 112})
        assert_expectations()

    def test_get_launch_ui_id(self, rp_service, monkeypatch):
        """Test get launch UI ID.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_get_launch_info = mock.Mock(return_value={'id': 113})
        monkeypatch.setattr(rp_service,
                            'get_launch_info',
                            mock_get_launch_info)
        assert rp_service.get_launch_ui_id() == 113

    def test_get_launch_ui_no_id(self, rp_service, monkeypatch):
        """Test get launch UI ID when no ID has been retrieved.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_get_launch_info = mock.Mock(return_value={})
        monkeypatch.setattr(rp_service,
                            'get_launch_info',
                            mock_get_launch_info)
        assert rp_service.get_launch_ui_id() is None

    def test_get_launch_ui_url(self, rp_service, monkeypatch):
        """Test get launch UI URL.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_get_launch_ui_id = mock.Mock(return_value=1)
        monkeypatch.setattr(rp_service,
                            'get_launch_ui_id',
                            mock_get_launch_ui_id)
        url = rp_service.get_launch_ui_url()
        assert url == '{0}/ui/#{1}/launches/all/1'.format(rp_service.endpoint,
                                                          rp_service.project)

    def test_get_launch_ui_url_no_id(self, rp_service, monkeypatch):
        """Test get launch UI URL no ID has been retrieved.

        :param rp_service:  Pytest fixture that represents ReportPortalService
                            object with mocked session.
        :param monkeypatch: Pytest fixture to safely set/delete an attribute
        """
        mock_get_launch_ui_id = mock.Mock(return_value=0)
        monkeypatch.setattr(rp_service,
                            'get_launch_ui_id',
                            mock_get_launch_ui_id)
        url = rp_service.get_launch_ui_url()
        assert url == '{0}/ui/#{1}/launches/all'.format(rp_service.endpoint,
                                                        rp_service.project)

    @mock.patch('reportportal_client.service._get_data',
                mock.Mock(return_value={'id': 123}))
    def test_start_item(self, rp_service):
        """Test for validate start_test_item.

        :param: rp_service: fixture of ReportPortal
        """
        rp_start = rp_service.start_test_item(name='name',
                                              start_time=1591032041348,
                                              item_type='STORY')
        expected_result = dict(json={'name': 'name',
                                     'description': None,
                                     'attributes': None,
                                     'startTime': 1591032041348,
                                     'launchUuid': 111,
                                     'type': 'STORY', 'parameters': None,
                                     'hasStats': True,
                                     'codeRef': None,
                                     'testCaseId': None},
                               url='http://endpoint/api/v2/project/item',
                               verify=True)

        rp_service.session.post.assert_called_with(**expected_result)
        assert rp_start == 123

    start_item_optional = [
        ('code_ref', '/path/to/test - test_item', 'codeRef',
         '/path/to/test - test_item'),
        ('attributes', {'attr1': True}, 'attributes',
         [{'key': 'attr1', 'value': 'True', 'system': False}])
    ]

    @pytest.mark.parametrize(
        'field_name,field_value,expected_name,expected_value',
        start_item_optional)
    @mock.patch('reportportal_client.service._get_data',
                mock.Mock(return_value={'id': 123}))
    def test_start_item_code_optional_params(self, rp_service, field_name,
                                             field_value, expected_name,
                                             expected_value):
        """Test for validate different fields in start_test_item.

        :param: rp_service:     fixture of ReportPortal
        :param: field_name:     a name of a field bypassed to
        rp_service.start_test_item method
        :param: field_value:    a value of a  field bypassed to
        rp_service.start_test_item method
        :param: expected_name:  a name of a field which should be in the result
        JSON request
        :param: expected_value: an exact value of a field which should be in
        the result JSON request
        """
        rp_service.start_test_item(name='name', start_time=1591032041348,
                                   item_type='STORY',
                                   **{field_name: field_value})
        expected_result = dict(json={'name': 'name',
                                     'description': None,
                                     'attributes': None,
                                     'startTime': 1591032041348,
                                     'launchUuid': 111,
                                     'type': 'STORY', 'parameters': None,
                                     'hasStats': True,
                                     'codeRef': None,
                                     'testCaseId': None},
                               url='http://endpoint/api/v2/project/item',
                               verify=True)
        expected_result['json'][expected_name] = expected_value
        rp_service.session.post.assert_called_with(**expected_result)
