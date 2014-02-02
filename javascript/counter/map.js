function(doc) {
  if (doc.name && doc.value && doc.type == "couchcrdt.counter.DistributedSet"){
    emit(doc.name, doc.value);
  }
}
