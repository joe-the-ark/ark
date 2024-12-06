# ark
The Ark is an Online Group Journey to develop your teams sense of psychological safety. It is developed by Dr. Joachim (Joe) Maier, Sempach, Switzerland and made available under GPLv3. Frontend made in Omsk with a backend from China. German / English / French / Chinese versions are playable via https://www.arks.ch
# 90 seconds preview video of the ARK online-journey
https://player.vimeo.com/video/852373658
# PDF-Intro to the ARK
https://www.dropbox.com/s/dljejtqlyc78gaq/22_10_ARK_Intro.pdf?dl=0
# The developers slidedeck on psychological safety
https://docs.google.com/presentation/d/1L-ZLyGT9G0aHv0Umj2poay6UOFBbWTpspAK0px_2DBQ/edit?usp=sharing
## Git Notes for backend and frontend developers
If you work on your local branches, make sure to do a `git pull origin master` before you merge your changes into the master branch or before you do a Pull-Request. This is very important to avoid merge conflicts.
## How to run the project 
- If you are developing on a Mac goto your terminal and run ```xcode-select --install``` to install xcode
- install brew by following the instructions via https://brew.sh/
- After the basic brew install, here are the two lines of code you need to run in your console…
```echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/maij/.profile```AND ```eval "$(/opt/homebrew/bin/brew shellenv)"```
- Install a current python (e.g. 3.x) & Django (e.g. 2.2.x) version.
- If you have not installed the meta library yet...
    - Please, under the ```meta/backend/src/``` directory, run ```python3 setup.py install``` to install the meta library.
    - If you have already installed the meta library, please continue to the next step.
- To update & compile the multi-language files (django.mo for french, english, chinese) under the ark directory, install gettext (Fedora: $ dnf install gettext-devel intltool / Ubuntu: $ sudo apt-get install gettext / Mac: $ brew install gettext AND $ brew link --force gettext) THAN type ```django-admin compilemessages``` in the terminal.
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
## Creator of the Game
* [Dr. Joachim Maier, creator of the game](https://www.linkedin.com/in/dr-joachim-maier/)
## Videos on Psychological Safety
* https://vimeo.com/482714127 (Amy Edmondson Creating Psychological Safety at Work)
* https://vimeo.com/482713162 (Psychological Safety talk with Steven Baert - Novartis - and Amy C. Edmondson - Harvard Business School)
* https://vimeo.com/459637793 (Charles Duhigg Asks What Makes a Great Team)
* https://vimeo.com/459639983 (How Google builds the perfect team)
* https://vimeo.com/459637808 (The Secret To Making Business Teams Successful)
* From Charles Duhigg – author of the newnowed 2016 New Yorker article on psychological safety https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html
## Links (Texts in German)
* Podcast Ark-Backstory & discussion of the safe-zone concept...
* https://lnkd.in/dxRNT-46
* Mein Blogbeitrag zu Psychologischer Sicherheit...
* https://blog.zhaw.ch/iap/2021/05/10/psychologische-sicherheit-wie-aufrichtig-kann-ich-in-meinem-team-kommunizieren/
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

## Troubleshooting for the installation:
Installing Meta Framework:
* If you see the message "No module named ’setuptools": # sudo apt-get install python3-setuptools
* If you see the message that „no suitable gcc“ available: # apt-get install build-essential
* If you see the message that headerfiles .h are missing: # apt-get apt-get install python3-dev

Installing Django:
* If there is no PIP: # apt-get install python3-pip

Possible further requirements:
* If gettext is missing: # apt-get install gettext 

If you run the server on a different IP adress and port than localhost, you want to edit ark/backend/backend/settings.py and settings_prod.py: 
DEBUG = TRUE 
ALLOWED_HOSTS = [‚XXX.XXX.XXX.XXX‘]   	with XXX… being your IP address.

If you want the server to listen to a different IP address, start it like this:
  python3 manage.py runserver XXX.XXX.XXX.XXX:PORT
