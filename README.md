# ark
The Ark is a social game to develop your teams sense of psychological safety. New ARK version. Frontend made in Omsk with a backend from China.
## Git Notes for backend and frontend developers
If you work on your local branches, make sure to do a `git pull origin master` before you merge your changes into the master branch or before you do a Pull-Request. This is very important to avoid merge conflicts.
## How to run the project 
- If you did't installed meta library yet
    - Please under the ```meta/backend/src/``` directory, run ```python3 setup.py install``` to install meta library.
    - If you have already installed it, please continue the step.
- Please under the ```backend/``` directory ( !!! not ```meta/backend/```!!! )
- If you are the first time to launch the backend
    - ```python3 manage.py migrate``` to create the database file
    - ```python3 manage.py runserver``` to run the server
    - Check ```localhost:8000``` in your browser
- Else if you are not the first time to launch the backend
    - ```python3 manage.py runserver``` to run the server
    - Check ```localhost:8000``` in your browser
- p.s.: you should run django 2.2
    - if you're on a higher version type anywhere in your console ```pip3 uninstall django```
    - then ```pip3 install django==2.2.```
