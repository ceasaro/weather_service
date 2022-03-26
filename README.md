# weather_service

#setup
###create postgis database
- create a virtual environment: create virtualenv (e.g. `mkvirtualenv --python=/usr/bin/python3 --no-site-packages weather_service`)
- `pip install -r setup/requirements-dev.txt`
- `createdb weather_service`

alternatively:
###develop in docker-compose
- `docker-compose -f docker-compose-dev.yml build`
- `docker-compose -f docker-compose-dev.yml up`
- you could be prompted for the docker-hub login credential.
- if everything works, you should have console output like:
```
[+] Running 2/0
 ⠿ Container django-fastapi-postgis-1   Created                                                                                                                                                               0.0s
 ⠿ Container django-fastapi-gunicorn-1  Recreated                                                                                                                                                             0.0s
Attaching to django-fastapi-gunicorn-1, django-fastapi-postgis-1
django-fastapi-postgis-1   | 2022-03-17 13:25:41.477 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
django-fastapi-postgis-1   | 2022-03-17 13:25:41.477 UTC [1] LOG:  listening on IPv6 address "::", port 5432
django-fastapi-postgis-1   | 2022-03-17 13:25:41.478 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
django-fastapi-postgis-1   | 2022-03-17 13:25:41.488 UTC [20] LOG:  database system was shut down at 2022-03-17 13:25:38 UTC
django-fastapi-postgis-1   | 2022-03-17 13:25:41.491 UTC [1] LOG:  database system is ready to accept connections
django-fastapi-gunicorn-1  | INFO:     Will watch for changes in these directories: ['/opt/weather_service']
django-fastapi-gunicorn-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
django-fastapi-gunicorn-1  | INFO:     Started reloader process [1] using statreload
django-fastapi-gunicorn-1  | INFO:     Started server process [8]
django-fastapi-gunicorn-1  | INFO:     Waiting for application startup.
django-fastapi-gunicorn-1  | INFO:     Application startup complete.
```
- open another shell and attach to the running app container with `docker exec -ti django-fastapi-app-1 bash` ("django-fastapi-app-1" can be different for your project)
- update dev requirements: `pip3 install -r setup/requirements-dev.txt`

###optional (mandatory for local machine)
- `cp weather_service/settings/local_settings_example.py weather_service/settings/local_settings.py`
  (and adjust to you local needs. If you use docker-compose, it should be fine)

###create tables and superuser
- `./manage migrate`
- `./manage collectstatic`
- `./manage.py createsuperuser`

###start uvicorn (optional, this is included in docker-compose-dev)
- `uvicorn weather_service.asgi:application --host 0.0.0.0 --port 8015 --reload`

goto http://localhost:8015/docs
goto http://localhost:8015/web/admin/

# Code conventions

For python, we use **black** for code formatting and a compatible 
**flask8**/pep8-naming check. The configuration is in the `.flake8` file and we use 
default black settings. Best is to use format-on-save for python files and install 
the pre-commit hook.

## How to use 

There are several options to use black and flake8.

- **CMD-line**: Run `black .` to format everything automatically, run `flake8` to 
  check for code compatibility
- **VSCode**; we have a `.vscode` directory with settings for _black format-on-save_. 

  _TODO_ check for flask8 automation here.
- **Pycharm** black save-on-format is complex. It's configurable through
  ‘external tools’, the formatting is done after save, but pycharm doesn't directly 
  update the reformatted file. see
  https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea

  _TODO_: check flake8 automation
- **Git commit hook**: We have the `pip pre-commit` package with the 
  `.pre-commit-config-yaml` file. Run `pre-commit install` for adding git hooks locally
  to avoid problems. Every commit is tested for black/flake8 compatibility. It's a bit
  cumbersome to test it in the service_skeleton template project because the `.flake8` 
  file is only used in the project root folder. If you instantiate the template, it
  will be used.
