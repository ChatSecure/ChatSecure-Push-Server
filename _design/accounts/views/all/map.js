function(doc) {
  if (doc.account_id) {
     emit(doc.account_id, doc);
  }
}