class Tag(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        response = self.client.make_request('/tags')
        response = response.json()
        return self.client._list_response(response)
