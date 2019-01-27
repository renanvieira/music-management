# Music Management App![](coverage.svg)
Rest API for manage music albums using SQLite, Python3.6 and Flask.


# Dependencies
* Python 3.6

# Remarks

TODO: about front-end
TODO: explain API

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

## Tests


### Running Tests
```bash
$ make run-tests
```

All API tests are located in [tests/](tests/)

### Test Coverage
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
Ran 20 tests in 2.065s

OK
```
