import mock
from unittest import TestCase
from toshl.client import ToshlClient
from toshl.account import Account
from toshl.exceptions import ToshlException


class TestAccount(TestCase):
    def test_account_init(self):
        client = ToshlClient('abcd1234')
        account = Account(client)
        assert account.client == client

    @mock.patch('toshl.client.requests.request')
    def test_list_accounts_successful(self, mock_request):
        mock_response = mock.Mock()
        expected_dict = {
            "id": "42",
            "name": "Account Test",
            "balance": 3000,
            "initial_balance": 3000,
            "currency": {
                "code": "USD",
                "rate": 1,
                "fixed": False
            },
            "median": {
                "expenses": 55,
                "incomes": 1300
            },
            "status": "active",
            "order": 0,
            "modified": "2012-09-04T13:55:15Z",
            "goal": {
                "amount": 63570,
                "start": "2013-07-01",
                "end": "2015-07-01"
            }
        }
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        response = account.list()

        mock_request.assert_called_once_with(
            headers={'Authorization': 'Bearer abcd1234'},
            method='GET', params=None, url='https://api.toshl.com/accounts')
        assert response == [expected_dict]

    @mock.patch('toshl.client.requests.request')
    def test_search_accounts_successful_multiple_accounts(self, mock_request):
        mock_response = mock.Mock()
        expected_dict = [
            {
                "id": "42",
                "name": "Account Test",
                "balance": 3000
            },
            {
                "id": "123",
                "name": "Test Found",
                "balance": 22000
            }
        ]

        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        account_found = account.search('Test Found')

        mock_request.assert_called_once_with(
            headers={'Authorization': 'Bearer abcd1234'},
            method='GET', params=None, url='https://api.toshl.com/accounts')
        assert account_found is not None
        assert account_found == '123'

    @mock.patch('toshl.client.requests.request')
    def test_search_accounts_successful_single_account(self, mock_request):
        mock_response = mock.Mock()
        expected_dict = {
            "id": "123",
            "name": "Test Found",
            "balance": 22000
        }

        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        account_found = account.search('Test Found')

        mock_request.assert_called_once_with(
            headers={'Authorization': 'Bearer abcd1234'},
            method='GET', params=None, url='https://api.toshl.com/accounts')
        assert account_found is not None
        assert account_found == '123'

    @mock.patch('toshl.client.requests.request')
    def test_search_accounts_not_found(self, mock_request):
        mock_response = mock.Mock()
        expected_dict = {
            "id": "123",
            "name": "Test Found",
            "balance": 22000
        }

        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        account_found = account.search('Not Found')

        mock_request.assert_called_once_with(
            headers={'Authorization': 'Bearer abcd1234'},
            method='GET', params=None, url='https://api.toshl.com/accounts')
        assert account_found is None

    @mock.patch('toshl.client.requests.request')
    def test_get_account_successful(self, mock_request):
        mock_response = mock.Mock()
        expected_dict = {
            "id": "42",
            "name": "Account Test",
            "balance": 3000,
            "initial_balance": 3000,
            "currency": {
                "code": "USD",
                "rate": 1,
                "fixed": False
            },
            "median": {
                "expenses": 55,
                "incomes": 1300
            },
            "status": "active",
            "order": 0,
            "modified": "2012-09-04T13:55:15Z",
            "goal": {
                "amount": 63570,
                "start": "2013-07-01",
                "end": "2015-07-01"
            }
        }
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        response = account.get('42')

        mock_request.assert_called_once_with(
            headers={'Authorization': 'Bearer abcd1234'},
            method='GET', params=None, url='https://api.toshl.com/accounts/42')
        assert response == expected_dict

    @mock.patch('toshl.client.requests.request')
    def test_account_not_found_raises_exception(self, mock_request):
        mock_response = mock.Mock()
        expected_dict = {
            'error_id': 'error.object.not_found',
            'description': 'Object with id 111 not found.'
        }
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 404
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')

        with self.assertRaises(ToshlException) as ex:
            client.make_request('/accounts/111', 'GET')

        assert ex.exception.status_code == 404
        assert ex.exception.error_id == 'error.object.not_found'
        assert ex.exception.error_description == 'Object with id 111 not found.'
        assert ex.exception.extra_info is None

    @mock.patch('toshl.client.requests.request')
    def test_create_account_successful(self, mock_request):
        mock_response = mock.Mock()
        mock_response.status_code = 201
        mock_response.headers = {'Location': '/accounts/1'}
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account_client = Account(client)

        json_payload = {
            'name': 'Test Account',
            'currency': {
                'code': 'GBP'
            }
        }

        response = account_client.create(json_payload)

        mock_request.assert_called_once_with(
            headers={
                'Authorization': 'Bearer abcd1234',
                'Content-Type': 'application/json'
            },
            method='POST', params=None, url='https://api.toshl.com/accounts',
            json=json_payload)
        assert response == '1'

    @mock.patch('toshl.client.requests.request')
    def test_update_account_successful(self, mock_request):
        json_payload = {
            'name': 'Test Account',
            'currency': {
                'code': 'GBP'
            },
            'extra': {
                'test': 'foo'
            }
        }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_payload
        mock_response.headers = {'Location': '/accounts/1'}
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account_client = Account(client)

        response = account_client.update('1', json_payload)

        mock_request.assert_called_once_with(
            headers={
                'Authorization': 'Bearer abcd1234',
                'Content-Type': 'application/json'
            },
            method='PUT', params=None, url='https://api.toshl.com/accounts/1',
            json=json_payload)
        assert response == json_payload

    @mock.patch('toshl.client.requests.request')
    def test_delete_account_successful(self, mock_request):
        mock_response = mock.Mock()
        mock_response.json.return_value = ''
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        response = account.delete('1')

        mock_request.assert_called_once_with(
            headers={'Authorization': 'Bearer abcd1234'},
            method='DELETE',
            params=None, url='https://api.toshl.com/accounts/1')
        assert response.json() == ''

    @mock.patch('toshl.client.requests.request')
    def test_move_account_successful(self, mock_request):
        json_payload = {
            'position': 2
        }

        mock_response = mock.Mock()
        mock_response.json.return_value = ''
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        response = account.move('1', 2)

        mock_request.assert_called_once_with(
            headers={
                'Authorization': 'Bearer abcd1234',
                'Content-Type': 'application/json'
            },
            method='POST',
            params=None, url='https://api.toshl.com/accounts/1/move',
            json=json_payload)
        assert response.json() == ''

    @mock.patch('toshl.client.requests.request')
    def test_reorder_account_successful(self, mock_request):
        accounts_list = ['3', '1', '2']

        json_payload = {
            'order': accounts_list
        }

        mock_response = mock.Mock()
        mock_response.json.return_value = ''
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        response = account.reorder(accounts_list)

        mock_request.assert_called_once_with(
            headers={
                'Authorization': 'Bearer abcd1234',
                'Content-Type': 'application/json'
            },
            method='POST',
            params=None, url='https://api.toshl.com/accounts/reorder',
            json=json_payload)
        assert response.json() == ''

    @mock.patch('toshl.client.requests.request')
    def test_merge_account_successful(self, mock_request):
        accounts_list = ['1', '2']
        dest_account = '2'

        json_payload = {
            'accounts': accounts_list,
            'account': dest_account
        }

        mock_response = mock.Mock()
        mock_response.json.return_value = ''
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        client = ToshlClient('abcd1234')
        account = Account(client)
        response = account.merge(accounts_list, dest_account)

        mock_request.assert_called_once_with(
            headers={
                'Authorization': 'Bearer abcd1234',
                'Content-Type': 'application/json'
            },
            method='POST',
            params=None, url='https://api.toshl.com/accounts/merge',
            json=json_payload)
        assert response.json() == ''
