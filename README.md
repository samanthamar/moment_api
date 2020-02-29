Usage 
* Update `config.py` with appropriate db details (NOTE: need to setup mysql server either locally or through Docker, please see Google doc)
* Start the server `run.py` 

Sample endpoints
* `GET localhost:5000/api/users`
* `POST localhost:5000/api/users`

Adding new Models 
* Define database models in `/models`
* Also define the schema here too for validation

Creating RESTful Endpoints 
* Each endpoint is listed in `app.py`
* Each endpoint requires a corresponding `resource` created in `/resources`

Requirements 
* `python 3.7`
* `pip3 install -r requirements.txt` 


