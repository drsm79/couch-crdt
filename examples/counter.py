from posixpath import join
from couchcrdt import DistributedCounter
from base import print_counter, server


c1 = DistributedCounter(
    'c1',
    join(server, 'crdt-demo/_design/crdt/_view/counter'),
    join(server, 'crdt-demo/'),
    always_write=True
)

print_counter(c1)  # A counter waiting for counts
c1.inc()
print_counter(c1)  # Local change only, but writes to the server
c1 + 10
print_counter(c1)  # Local change only, but writes to the server
print 'c1.state (should be 11 - local state only):', c1.state
print 'c1.value (should be None - not contacted server yet):', c1.value
c1.get()  # Read the distributed state from the server
print_counter(c1)

# Now have two counters writing to the same name
clone_c1 = DistributedCounter(
    'c1',
    join(server, 'crdt-demo/_design/crdt/_view/counter'),
    join(server, 'crdt-demo/'),
    always_write=False
)

clone_c1.get()  # Get the server value
c1 + 10  # increment c1 and the server (always_write=True)
print "c1 should be 10 ahead of clone_c1"
print_counter(c1)
print_counter(clone_c1)

clone_c1 + 10
print "c1 should be equal to clone_c1"
print_counter(c1)
print_counter(clone_c1)

clone_c1.put()
clone_c1.get()
print "c1 should be 10 behind of clone_c1"
print_counter(c1)
print_counter(clone_c1)

c1.get()
print "c1 should be equal to clone_c1"
print_counter(c1)
print_counter(clone_c1)
