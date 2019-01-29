# Music Management App![](coverage.svg) 
Rest API for manage music albums.


# Dependencies
* Python 3.6

# Remarks

## Backend
I built the backend API using Flask and SQLite. SQLAlchemy as ORM and Marshmallow for data validation and marshalling.

Generally, I would use a repository pattern for data access, but due to simplicity of the queries and the lack of the need of reuse the same query, 
I prefered keep it simple and inside the route function.

### Tests [](coverage-api.svg)
The API is with a Test Coverage of 99%. The tests can be runned with the following command:
```bash
make run-api-tests
```
You should see the following output: 
```text
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
music_management/__init__.py                       0      0   100%
music_management/app.py                           48      1    98%
music_management/config.py                        37      0   100%
music_management/db.py                             2      0   100%
music_management/extensions.py                     4      0   100%
music_management/helpers.py                        8      0   100%
music_management/middleware.py                     4      0   100%
music_management/models.py                        11      0   100%
music_management/resources/__init__.py             0      0   100%
music_management/resources/album/__init__.py       0      0   100%
music_management/resources/album/routes.py        84      0   100%
music_management/resources/album/schemas.py       24      0   100%
music_management/resources/error.py               31      2    94%
music_management/resources/ping.py                 4      0   100%
------------------------------------------------------------------
TOTAL                                            257      3    99%
----------------------------------------------------------------------
Ran 58 tests in 2.490s

OK
```
All API tests are located [here](tests/api).


## Frontend
Here is where I struggled due to my lack of experience on frontend javascript frameworks. I wasn't able to learn the React concepts in so short notice, so I built another Flask application for the frontend using just one extension to help handle the form.

I even started the frontend using React but, after a few hours trying to get something to work, I decide to use a simpler approach using the tools I already know.  



### Tests [](coverage-web.svg)
The Web application is with a Test Coverage of 94%. The tests can be runned with the following command:
```bash
make run-web-tests
```
You should see the following output: 
```text
Name                              Stmts   Miss  Cover
-----------------------------------------------------
web/__init__.py                       0      0   100%
web/app.py                           43      1    98%
web/config.py                        30      0   100%
web/extensions.py                     2      0   100%
web/models.py                        24      0   100%
web/resources/__init__.py             0      0   100%
web/resources/album/__init__.py       0      0   100%
web/resources/album/routes.py       121     12    90%
web/resources/error.py               13      2    85%
web/resources/ping.py                 4      0   100%
web/services.py                      82      4    95%
-----------------------------------------------------
TOTAL                               319     19    94%
----------------------------------------------------------------------
Ran 58 tests in 3.536s

OK
```
All API tests are located [here](tests/web).

# Usage

## Starting application 

### Docker

The project has a `docker-compose` with both application (web and api) ready to run, you can use the `docker-compose up`
or use the shortcut in the `Makefile` as shown below.

```bash
$ make start-docker
```

#### Containers
   * `web`: Web app running on port [`8085`](http://localhost:8085)
   * `api`: API running on port [`5000`](http://localhost:5051)

If you need to stop/remove the containers use the following command:
```bash
$ make stop-docker
```

## Tests [](coverage.svg)
To run all tests, use the following command:
```bash
make run-tests
```
