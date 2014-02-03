import json
from crdt import CRDT
from collections import Counter

"""
operation       | item in external set | item not in external set
----------------+----------------------+--------------------------
('a', 'd', 'd') | delete item          | delete item (no op)
('d', 'a', 'd') | delete item          | delete item (no op)
('d', 'd', 'a') | add item             | add item
('a', 'a', 'd') | delete item          | delete item (no op)
('a', 'd', 'a') | no op                | add item
('d', 'a', 'a') | no op                | add item
"""


class DistributedSet(CRDT):
    def __init__(self, name, url, db, auth=(), params={}, always_write=False):
        super(DistributedSet, self).__init__(
            name,
            url,
            db,
            auth,
            params,
            always_write
        )
        if 'cloudant.com' not in url:
            del self.params['key']
            self.params['startkey'] = json.dumps([name])
            self.params['endkey'] = json.dumps([name, {}])
        self.additions = Counter()
        self.deletions = Counter()
        self.value = set()
        self.default_state = set()

    def add(self, item):
        self.additions[item] += 1

    def remove(self, item):
        # Have to add here because we use counter subtraction below
        self.deletions[item] += 1

    def __iter__(self):
        """
        Do the set operation and return the iterable over the result
        """
        adds, deletes = self._get_state()
        return iter(
            self.value.union(set(adds)) - set(deletes)
        )

    def __str__(self):
        adds, deletes = self._get_state()
        return str(
            self.value.union(set(adds)) - set(deletes)
        )

    def _update(self, item):
        """
        The _update method on a DistributedSet is only used to reset internal
        state to their original state.
        """
        self.additions = Counter()
        self.deletions = Counter()

    def _get_state(self):
        adds = self.additions - self.deletions
        deletes = self.deletions - self.additions
        return adds, Counter(dict((k, -1 * v) for k, v in deletes.iteritems()))

    def _serialise(self):
        adds, deletes = self._get_state()
        return {
            'additions': adds,
            'deletions': deletes
        }

    def _parse(self, data):
        if 'cloudant.com' in data.url:
            data = data.json()['rows'][0]['value']
            return set([k for k, v in data.iteritems() if v > 0])
        else:
            s = set()
            for row in data.json()['rows']:
                if row['value'] > 0:
                    s.add(row['key'][1])
            return s
