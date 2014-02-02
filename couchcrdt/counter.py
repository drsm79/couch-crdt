from crdt import CRDT


class DistributedCounter(CRDT):

    def add(self, number):
        return self + number

    def remove(self, number):
        return self - number

    def inc(self):
        """
        Increase the counters value by one
        """
        return self + 1

    def dec(self):
        """
        Reduce the counters value by one
        """
        return self - 1

    def __abs__(self):
        """
        Do the set operation and return the iterable over the result
        """
        if self.state is None:
            return self.value
        if self.value is None:
            return self.state
        return self.value + self.state

    def __repr__(self):
        return "%s" % self.__abs__()

    def __add__(self, number):
        if isinstance(self.state, (int, long, float, complex)):
            self._update(self.state + number)
        else:
            self._update(number)
        return self

    def __sub__(self, number):
        if isinstance(self.state, (int, long, float, complex)):
            self._update(self.state - number)
        else:
            self._update(-number)
        return self

    def _parse(self, data):
        return data.json()['rows'][0]['value']
