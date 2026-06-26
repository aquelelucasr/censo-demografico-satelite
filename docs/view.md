GUI built with tkinter, able to request dynamic data from the controller for real time requests or request previous data from the database


## TODOS:
 
- [X] main view ← program start
- displays a map and allows the user to write down coordinates or select two points on the map that form a square
- [X] text boxes for manual latitude and longitude selection
- [ ] submit button that calls the controller and creates a new request in the database
- [ ] **_OPTIONAL_** make the user able to select points through the map, updating the input boxes
- [ ] **_OPTIONAL_** move and display a pin on the map when the user types a new coordinate in manually
- [ ] submitting redirects to a detail view to display the data
---
- [ ] search history 
- lists old requests saved in the database
- [ ] use the get-all function from the local MODEL package to create a list of all the requests
- [ ] allow the user to select one to see details in a detail view
- [ ] allow the user to delete an entry with a button 
 ---
- [ ] detail view
- displays data from a request (present or past) 
- shows labeled image FILEPATH given by the database
- display all data from request TODO: define specifics