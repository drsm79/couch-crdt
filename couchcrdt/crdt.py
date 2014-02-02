import requests
import json


class CRDT(object):
    """
    A base class CRDT. This only takes care of getting the value and putting
    the local state of the CRDT from/to the database. What those things mean is
    up to specific implementations.
    """
    def __init__(self, name, url, db, auth=(), params={}, always_write=False):
        """
        name: an identifier for the crdt, translates to a key in a CouchDB view

        url: the full url of the crdt, e.g. a named view

        db: the url of the database

        auth: a tuple of (username, password)

        params: a dict of additional query string parameters to send
        to the view

        always_write: write out the state of the CRDT
        """
        self.name = name
        self.url = url
        self.database = db
        self.session = requests.Session()
        self.session.auth = auth
        self.session.headers = {
            'User-Agent': 'couchcrdt/0.0.1',
            'Content-Type': 'application/json'
        }
        p = {'reduce': True, 'group': True, 'key': self.name}
        p.update(params)
        self.params = dict((k, json.dumps(v)) for k, v in p.iteritems())
        self.value = None
        self.state = None
        self.always_write = always_write
        self.default_state = None

    def get(self):
        """
        Get the latest value from the database for the CRDT and eliminate local
        state.
        """
        r = self.session.get(self.url, params=self.params)
        r.raise_for_status()
        self.value = self._parse(r)
        self._update(self.default_state)

    def put(self):
        """
        Write the CRDT's local state (not it's value) to the database
        """
        r = self.session.post(
            self.database,
            json.dumps({
                'value': self._serialise(),
                'name': self.name,
                'type': '.'.join([
                    self.__class__.__module__,
                    self.__class__.__name__
                ])
            })
        )
        r.raise_for_status()

    def _update(self, state):
        """
        Update the local state
        """
        self.state = state
        if self.always_write:
            self.put()

    def _get_state(self):
        """
        Return the internal, local only state
        """
        return self.state

    def _parse(self, data):
        return data.json()['rows'][0]['value']

    def _serialise(self):
        """
        Return the externalised state of the CRDT, defaults to the local state
        """
        return self._get_state()
