# Blog Rest API by flask with JWT auth 

Blog API with CRUD operation, bulid with Flask, FLask-Restful and Flask_SQLAlchemy. Blog post store in database with fields of title, author, content and database generated id. Title must be unique. User doesn't need to know the id for a blog, when posting a blog, a url for the blog will return to user for future access.

The blog pages are protected, before view any page, user needs register. The register and login process use JWT token instead of cookie session, in accordance with REST style.

Below is explanations and test methods for operations.

## Install
virtualenv -p python3 venv\
source venv/bin/activate\
pip install -r requirements.txt

## Start server
You can start server with :

`FLASK_APP=run.py FLASK_DEBUG=1 flask run`

## User registration
The blog pages are protected, before view any page, user needs register, here use curl command for example to test:

`curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test", "password":"test"}' http://localhost:5000/registration`

## User login
Use registered user and password to login:

`curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test", "password":"test"}' http://localhost:5000/login`

The API will return an access token and a refresh token.

## View all blogs
Use returned access token to view blog page:

`curl -i -H "Authorization:Bearer <your access token>"  http://localhost:5000/blogapi/v1.0/blogs`

## Refresh Token
The access token will expire after 15 minutes, when that happens, refresh the user with refresh token.

`curl -i -H "Authorization:Bearer <your refresh token>" -X POST http://localhost:5000/token/refresh`

## View specific blogs
`curl -i -H "Authorization:Bearer <your access token>"  http://localhost:5000/blogapi/v1.0/blogs/3`

## Post new blog
`curl -i -H "Authorization:Bearer <your access token>" -H "Content-Type: application/json" -X POST -d '{"title":"How to"}' http://localhost:5000/blogapi/v1.0/blogs`

## Update a blog
`curl -i -H "Authorization:Bearer <your access token>" -H "Content-Type: application/json" -X PUT -d '{"title":"head","content":"content"}' http://localhost:5000/blogapi/v1.0/blogs/5`

## Delete a blog
`curl -i -H "Authorization:Bearer <your access token>" -X DELETE  http://localhost:5000/blogapi/v1.0/blogs/5`

## User logout
When user logout, the access token will be added to a blacklist. 

Test logout using access token:

`curl -i -H "Authorization:Bearer <your access token>" -X POST http://localhost:5000/logout/access`

Test logout using refresh token:

`curl -i -H "Authorization:Bearer <your access token>" -X POST http://localhost:5000/logout/refresh`



