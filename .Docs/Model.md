Responsible for keeping track of previous requests done to the system


## TODOS:
- [ ] Implement all tables and respective cr~~u~~ds
  - [x] Requests
    - [x] create
    - [x] read
    - [x] delete
  - [ ] RequestData
    - [ ] create
    - [ ] read
    - [ ] update
    - [ ] ~~delete~~ RequestData should only be deleted when the associated request is deleted, so implement this in RequestData's delete function!

### current tables:

```
Tablename: 
- search_history
Fields:
- id INTEGER PRIMARY KEY AUTOINCREMENT,
- slug   STRING
- lat_tl FLOAT
- lon_tl FLOAT
- lat_br FLOAT
- lon_br FLOAT

Tablename:
- request_data
Fields:
- id INTEGER PK FK // if you can you have a primary key be a foreign key otherwise split these up!
- population    INTEGER
- pop_density   FLOAT
... TODO: ADD ANYTHING ELSE REQUIRED!
```

