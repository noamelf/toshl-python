from functools import partial


class Tag(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        partial_request = partial(self.client.pagination_partial_request, url="/tags")
        return self.client.pagination_helper(partial_request)
