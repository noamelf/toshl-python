import logging

logger = logging.getLogger(__name__)


class Entry(object):
    def __init__(self, client):
        self.client = client

    def _list_pagination(self, from_date, to_date, page):
        response = self.client.make_request(
            "/entries", params={"from": from_date, "to": to_date, "page": page}
        )
        return response

    def list(self, from_date, to_date):
        page = 0
        entries = []
        while True:
            response = self._list_pagination(from_date, to_date, page)
            entries.extend(response.json())
            if "next" not in response.links:
                break
            page += 1

        return entries

    def create(self, json_payload):
        response = self.client.make_request("/entries", "POST", json=json_payload)
        if response.status_code == 201:
            return self.client._parse_location_header(response)

    def get(self, entry_id):
        return self.client.make_request(f"/entries/{entry_id}").json()

    def put(self, entry):
        response = self.client.make_request(
            f"/entries/{entry['id']}", "PUT", json=entry
        )
        response.raise_for_status()
        logger.info(f'Updated entry: {entry["id"]}')
