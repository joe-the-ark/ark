# ark
The Ark is an Online Group Challenge to develop your teams sense of psychological safety. It is developed by Dr. Joachim Maier, Sempach, Switzerland and made available under GPLv3. Frontend made in Omsk with a backend from China. German version is playable via https://www.arks.ch
## Git Notes for backend and frontend developers
If you work on your local branches, make sure to do a `git pull origin master` before you merge your changes into the master branch or before you do a Pull-Request. This is very important to avoid merge conflicts.
## How to run the project 
- If you have not installed the meta library yet...
    - Please, under the ```meta/backend/src/``` directory, run ```python3 setup.py install``` to install the meta library.
    - If you have already installed the meta library, please continue to the next step.
- To update & compile the multi-language files (django.mo for french, english, chinese) under the ark directory, type “django-admin compilemessages” in the terminal.
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
https://www.dropbox.com/s/cc6c58ix6zp8mtl/ARK_2_Gameflow.pdf?dl=0
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
## Links (Texts in German)
* Mein Foliensatz zu Psychologischer Sicherheit...
https://www.dropbox.com/s/dme4jm2q556mbwt/2021_Psychologische_Sicherheit.pdf?dl=0
* Guter halbwissenschaftlicher Einführungsartikel zu Psychologischer Sicherheit https://www.artop.de/psychologische-sicherheit-das-fundament-gelingender-arbeit-im-team/
* Clip1: Wie kam ich zur psychologischen Sicherheit? (3:16 Min.)
https://youtu.be/jiWCvz_nJm0
* Clip 2: Warum ist psychologische Sicherheit in aller Munde? (5:54 Min.)
https://youtu.be/vr-wa_FWgFE
* Clip 3: Was sind die Google Dimensionen psychologischer Sicherheit? (9:19 Min.)
https://youtu.be/fRMJbU9CiD4
* Clip 4: Für wen ist die Online Challenge die Arche geeignet? Wie kann ich die Arche nutzen? Wie spielen innere Zensur, psychologische Sicherheit und die Arche zusammen? (10:04 Min.)
https://youtu.be/H0WkHyPhdps
* Clip 5: Über das Bedürfnis gemeinsam unterwegs zu sein und einem angemessenen Umgang mit der Vielgestaltigkeit gruppendynamischer Prozesse. (7:33 Min.)
https://youtu.be/O--N9XMrRcw
* Digitec Galaxus Intervew zu heiligen Kühen [Interview bei Digitec Galaxus](https://www.personal-schweiz.ch/experten-interviews/article/innovation-bei-digitec-galaxus-gibt-es-keine-heiligen-kuehe/)
* Angebotsskizze für den Einsatz der Arche in Unternehmen [Short flyer about the game](https://www.ywesee.com/uploads/Arks/Arks_The_Game.pdf)
