# cteemo
* website http://www.cteemo.com/

## Requirements
* Flask
* Flask-RESTful==0.3.1
* flask-mongoengine==0.7.1
* flask-redis==0.0.6
* flask-bcrypt
* flask-mail
* itsdangerous==0.24
* requests 
* gunicorn
* boto
* rongcloud
* challonge

## Quick Start
Use command gunicorn -c gunicorn.py app:app to start the server. Note that the server will automatically reload the latest code deployment. Use log/error.log and log/access.log to find logging information and debug. Configuration of gunicorn can be found at gunicorn.py. Configuration of [MongoDB](http://docs.mongodb.org/ecosystem/drivers/python/) and [Redis](http://redis.io/documentation) can be found at config.py. Information about routing and urls can be found at app.py.

## Database Models
Database designs are located at the folder 'model'. A class inherited from 'db.Document' of Mongoengine is a table in MongoDB. The primary key is id (objectId) by default. Queries are typically performed on primary keys and unique keys by calling the method 'objects(...)'. ReferenceField is used to reference to another object in a different (or the same) table. Mongoengine will do dereferencing by default. After updating the database, don't forget to save the changes you made. Also, make sure the whole process is atomic by either using functions provided by Mongoengine or writing your own. 
Read [mongoengine](http://docs.mongoengine.org/en/latest/apireference.html) API for further information.

## API
APIs can handle [HTTP requests](http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html) sent to the server. [JSON](https://docs.python.org/2/library/json.html) is used for communication. Raise InvalidUsage exception when there is an illegal request. If there is a need for returning more information than just the status, find templates of serialize a JSON at util/serialize.py

## Github & Deployment
Before writing any code, first synchronize with the master branch. Typically we need a seperate branch for one issue but it's not necessary now...
When you are done, push the commit to github then use the shell to login to server and pull the code from github. This is the current deployment step. 
