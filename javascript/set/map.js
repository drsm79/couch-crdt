function(doc) {
  if (doc.type=="couchcrdt.dset.DistributedSet" && doc.value && doc.name){
    Object.keys(doc.value.deletions).forEach(function (k) {
      emit([doc.name, k], doc.value.deletions[k]);
    });
    Object.keys(doc.value.additions).forEach(function (k) {
      emit([doc.name, k], doc.value.additions[k]);
    });
  }
}
