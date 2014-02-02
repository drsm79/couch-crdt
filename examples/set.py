from posixpath import join
from couchcrdt import DistributedSet
from base import server

print 'hello!'

s = DistributedSet(
    's1',
    join(server, 'crdt-demo/_design/crdt/_view/set'),
    join(server, 'crdt-demo/'),
    always_write=True
)

s.add('fred')
s.add('bob')
s.add('sarah')
s.add('jane')
print s
s.remove('bob')
print s
s.put()

cloned_s = DistributedSet(
    's1',
    join(server, 'crdt-demo/_design/crdt/_view/set'),
    join(server, 'crdt-demo/'),
    always_write=True
)
cloned_s.add('guillaume')
cloned_s.add('bill')
cloned_s.add('william')
cloned_s.remove('fred')
print cloned_s
cloned_s.put()
cloned_s.get()
print cloned_s
