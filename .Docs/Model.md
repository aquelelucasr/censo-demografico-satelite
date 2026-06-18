## Responsible for keeping track of previous requests done to the system


### TODO:

- [ ] Implement all tables and respective CRUDs
  - [ ] Implement `search_history` table
    - [x] create (`save_search()`)
    - [x] read (both `find_search_by_term()` and `get_all_history()`)
    - [ ] delete
  - [ ] Implement `search_results` table
    - [x] create
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
- lat_tl REAL
- lon_tl REAL
- lat_br REAL
- lon_br REAL

Tablename:
- request_data
Fields:
- id INTEGER PK FK // if you can you have a primary key be a foreign key otherwise split these up!
- population    INTEGER
- pop_density   REAL
... TODO: ADD ANYTHING ELSE REQUIRED!
```

