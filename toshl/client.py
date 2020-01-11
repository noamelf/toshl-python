from functools import partial

import requests

from .exceptions import ToshlException


class ToshlClient(object):
    BASE_API_URL = 'https://api.toshl.com'

    def __init__(self, token):
        self._token = token

    def make_request(
            self, api_resource, method='GET', params=None, **kwargs):
        """
        Shortcut for a generic request to the Toshl API
        :param url: The URL resource part
        :param method: REST method
        :param parameters: Querystring parameters
        :return: requests.Response
        """
        if kwargs.get('json'):
            headers = {
                'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/json'
            }
        else:
            headers = {
                'Authorization': 'Bearer {}'.format(self._token)
            }

        response = requests.request(
            method=method,
            url='{0}{1}'.format(self.BASE_API_URL, api_resource),
            headers=headers,
            params=params,
            **kwargs
        )

        if response.status_code >= 400:
            error_response = response.json()

            raise (ToshlException(
                status_code=response.status_code,
                error_id=error_response['error_id'],
                error_description=error_response['description'],
                extra_info=error_response.get('fields')))

        return response

    def _list_response(self, response):
        """
        This method check if the response is a dict and wrap it into a list.
        If the response is already a list, it returns the response directly.
        This workaround is necessary because the API doesn't return a list
        if only one item is found.
        """
        if type(response) is list:
            return response
        if type(response) is dict:
            return [response]

    def _parse_location_header(self, response):
        return response.headers['Location'].split('/')[-1:][0]

    def pagination_partial_request(self, url, page, from_date=None, to_date=None):
        if from_date and to_date:
            return self.make_request(url, params={"from": from_date, "to": to_date, "page": page})
        return self.make_request(url, params={"page": page})

    @staticmethod
    def pagination_helper(http_request_fn):
        page = 0
        entries = []
        while True:
            response = http_request_fn(page=page)
            entries.extend(response.json())
            if "next" not in response.links:
                break
            page += 1

        return entries
