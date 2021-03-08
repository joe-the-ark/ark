# ark
The Ark is a social game to develop your teams sense of psychological safety. It is developed by Dr. Joachim Maier, Sempach, Switzerland and made available under GPLv3. Frontend made in Omsk with a backend from China.
## Git Notes for backend and frontend developers
If you work on your local branches, make sure to do a `git pull origin master` before you merge your changes into the master branch or before you do a Pull-Request. This is very important to avoid merge conflicts.
## How to run the project 
- If you have not installed the meta library yet...
    - Please, under the ```meta/backend/src/``` directory, run ```python3 setup.py install``` to install the meta library.
    - If you have already installed the meta library, please continue to the next step.
- Please goto the ```backend/``` directory ( !!! not ```meta/backend/```!!! )
- If you are launching the backend for the first time type
    - ```python3 manage.py migrate``` to create the database file
    - ```python3 manage.py runserver``` to run the server
    - Check ```localhost:8000``` in your browser
- Else if you are not launching the backend for the first time type
    - ```python3 manage.py runserver``` to run the server
    - Check ```localhost:8000``` in your browser
- p.s.: you should run django 2.2
    - if you're on a higher version type anywhere in your console ```pip3 uninstall django```
    - then ```pip3 install django==2.2.13```
## The Gameflow in a Nutshell
- Overview of the 18 steps in the gameflow
https://www.dropbox.com/s/hpss180nj2dpeem/ARK_3_Gameflow.pdf?dl=0
- Detailed overview in multiple languages (German, English, French, Chinese, Russian)
https://www.dropbox.com/s/u3zk2dun9pw8ug9/ARK_2_Gameflow_Overview.pdf?dl=0
- 60 seconds game_preview video
https://vimeo.com/488263813
## Creator of the Game
* [Dr. Joachim Maier, creator of the game](https://www.linkedin.com/in/dr-joachim-maier/)
* [Some pictures The ARKS backstory](https://photos.app.goo.gl/4fHKgDkx9ChjeiuV8)
## Videos on Psychological Safety
* https://vimeo.com/482714127 (Amy Edmondson Creating Psychological Safety at Work)
* https://vimeo.com/482713162 (Psychological Safety talk with Steven Baert - Novartis - and Amy C. Edmondson - Harvard Business School)
* https://vimeo.com/459637793 (Charles Duhigg Asks What Makes a Great Team)
* https://vimeo.com/459639983 (How Google builds the perfect team)
* https://vimeo.com/459637808 (The Secret To Making Business Teams Successful)
* From Charles Duhigg – author of the newnowed 2016 New Yorker article on psychological safety https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html
## Links
* https://www.artop.de/psychologische-sicherheit-das-fundament-gelingender-arbeit-im-team/
* [Interview bei Digitec Galaxus](https://www.personal-schweiz.ch/experten-interviews/article/innovation-bei-digitec-galaxus-gibt-es-keine-heiligen-kuehe/)
* [Short flyer about the game](https://www.ywesee.com/uploads/Arks/Arks_The_Game.pdf)
* [Youtube Channel of Joachim about the game](https://www.youtube.com/playlist?list=PLrbFdfg38GXmg3jyMz_OYNilscbO_FDiH)
