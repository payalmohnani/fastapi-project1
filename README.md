# fastapi-project1
**"fastapi-project1"** is my first **REST API** backend development project which I created by following the youtube tutorial by @Sanjeev-Thiyagarajan . It is a social media type application which performs basic social media like operations(**CRUD**-based API). 

It has 2 main parts : Posts and Users.

For Posts, it allows  HTTP requests like: Post(Create a post and vote/unvote an existing post), Get(request multiple posts by query or a single post by id), Put(Update) and Delete.

For Users, it allows Post(Create a user) and Get(get info about the user).

It also performs user authentication using **JWT token**.

## Techstack Used:
FastAPI

PostgreSql Database 

SQLAlchemy to query Database

Alembic for database migration

The project is deployed on **Render**.

## Link to the API
Further information regarding project are in the project documentation on the link below:

[API project Swagger UI](https://simple-fastapi-project.onrender.com/docs#)

[API project redoc](https://simple-fastapi-project.onrender.com/redoc)
