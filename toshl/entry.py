import logging
from functools import partial

logger = logging.getLogger(__name__)


class Entry(object):
    def __init__(self, client):
        self.client = client

    def list(self, from_date, to_date):
        partial_request = partial(
            self.client.pagination_partial_request,
            url="/entries",
            from_date=from_date,
            to_date=to_date,
        )
        return self.client.pagination_helper(partial_request)

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

    def update_entry(self, entry_id, **updates: dict):
        entry: dict = self.get(entry_id)
        entry.update(updates)
        self.put(entry)
