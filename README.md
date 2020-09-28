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
## The Gameflow in a Nutshell
https://www.dropbox.com/s/cc6c58ix6zp8mtl/ARK_2_Gameflow.pdf?dl=0
## Creator of the Game
* [Dr. Joachim Maier, creator of the game](https://www.linkedin.com/in/dr-joachim-maier/)
* [Some pictures how the Game was developed](https://photos.app.goo.gl/4fHKgDkx9ChjeiuV8)
## Videos on Psychological Safety
* https://vimeo.com/459637793 (Charles Duhigg Asks What Makes a Great Team)
* https://vimeo.com/459639983 (How Google builds the perfect team)
* https://vimeo.com/459637808 (The Secret To Making Business Teams Successful)
* From Charles Duhigg – author of the newnowed 2016 New Yorker article on psychological safety https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html
## Links
* https://www.artop.de/psychologische-sicherheit-das-fundament-gelingender-arbeit-im-team/
* [Interview bei Digitec Galaxus](https://www.personal-schweiz.ch/experten-interviews/article/innovation-bei-digitec-galaxus-gibt-es-keine-heiligen-kuehe/)
* [Short flyer about the game](https://www.ywesee.com/uploads/Arks/Arks_The_Game.pdf)
* [Youtube Channel of Joachim about the game](https://www.youtube.com/playlist?list=PLrbFdfg38GXmg3jyMz_OYNilscbO_FDiH)
* [Simple youtube Video about the Game](https://www.youtube.com/watch?v=zeckcko3a8w&feature=youtu.be)
