function(doc) {
  if (doc.type=="couchcrdt.dset.DistributedSet" && doc.value && doc.name){
    emit(doc.name, doc.value.deletions);
    emit(doc.name, doc.value.additions);
  }
}
