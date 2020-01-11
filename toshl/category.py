from functools import partial


class Category(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        partial_request = partial(self.client.pagination_partial_request, url="/categories")
        return self.client.pagination_helper(partial_request)

    def search(self, category_name):
        categories = self.list()
        for c in categories:
            if c['name'] == category_name:
                return c['id']
