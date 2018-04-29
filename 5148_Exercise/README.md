# Notes on `mongo`
> **Contents**
1. `mongo` basic
2. `mongo` shell

## 1. `mongo` basics

### 1.1 `mongo` data structure –– BSON

**MongoDB** uses **JSON**(JavaScript Object Notation) doucuments in binary-encoded format, which provides many different types and more complicated structure. **BSON** or Binary JSON, extends the JSON model to provide additional data types. 

**Example of JSON**
```JSON
{"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}
```
**Compare with BSON**
```BSON
{"_id":123,
 "name":{
     "first":"first name",
     "last":"last name"
 },
 "age":29,
 "Belongings":[
     {"item":"shoes", "value":200},
     {"item":"bicycle", "value":800},
     {"item":"briefcase", "value":1500}
 ]
}
```

## 1.2 Basic CRUD in `mongo`
### 1.2.1 Creation
To create a new database, a new collection, a new document
* `use <database>`: switch to another database. If it doesn't exist, it will initialise a new database.
* `db.createCollection(<collection>)`: initialise a new collection.
* Using variable to temporarily store a document:
```mongo
> var new = {"sid":123,
...            "name":"David",
...            "info":{"year":2018, "mark":90}
...            }
> db.collection.insert(new)
```

### 1.2.2 Read
* `find()`: return the result of a query. Without given parameter, it will by default return the entire documents in a collection.  
```mongo
> db.collection.find()
```
* `count()`: return the number of documents.
* `sort()`: sort the documents by criteria. `1` for ascending, `-1` for descending.
```mongo
> db.collection.find().sort({"_id":1})
{"_id":123, ...}
{"_id":124, ...}
...
```
* `limit()`: limit the documents to retrieved. No limit if parameter is not given.
* `hasNext()` and `next()`:  
Considering the following codes:
```shell
> var results = db.collection.find({"unit_code":"FIT5148"})
> results.hasNext() #Check whether it is empty.
true
> results.count()
2
> results.next()
{"sid":1, ...}
> results.next()
{"sid":2, ...}
> results.hasNext()
false
> results.count()
2
> results.next()
2018-04-28T22:42:53.058+1000 E QUERY    [thread1] Error: error hasNext: false :
DBQuery.prototype.next@src/mongo/shell/query.js:305:1
@(shell):1:1
```
Now we can see that the `results` variable stores the output of the `find()`. It works as a generator in Python  but "pop" the first document out when execute `next()` function and remember where it ends. It is noteworthy to notice that `count()` only retrieve the number of documents in this variable(which seem to be immutable after the variable has been initialised).  
* `print()`: print out the document.
* `pretty()` or `printjson()`: print out in a more readable style.
* `explain()`: it usually take `"allPlansExecution"` as its parameter. More infomation in **Indexing**.