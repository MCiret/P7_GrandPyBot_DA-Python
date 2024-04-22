================================
"GrandPy bot" (learning) project
================================
**Searching for a spot address**

🔗 https://grandpybot.p7.mc-dapy.fr/

|Status badge| |vPython badge|
|UIlanguage badge| |vHTML badge| |vCSS badge| |JavaScript badge|

*****************
TABLE OF CONTENTS
*****************

1. `DESCRIPTION`_
    * `Learning project`_
    * `Summary`_
    * `Feature and scenario`_

2. `INSTALLATION`_
    * `Steps`_
    * `Required libraries`_

3. `USAGE`_
    * `UI example`_
    * `API data`_


DESCRIPTION
===========

Learning project
----------------
This Web app has been developed during OpenClassrooms training course "Python Application Development".

**GOAL** :

* very 1st Web app using Flask framework (minimalist : 1 route, no DB, no tests)
* AJAX + HTML/CSS basics
* "Like NLP" logic/algo (option : use a third library --> SpaCy had been chosen)
* Third API calls

Summary
-------
User could ask (french only) for locating a place to user by entering a question in an text input field and submit it.

A robot (GrandPy Bot) parses (tiny NLP) user input and requests 2 API :

* HERE.com to get the address and pinned it on a map,
* Wikipedia to get infos article (intro + url are displayed).


Feature and scenario
--------------------
A user could asks GrandPy Bot a place name in order to obtain the address.

1) User asks GrandPy Bot a place name that is locatable by here.com and have a Wikipedia article.

    **Given** I am a user who is asking for a place address,

    **When** GrandPy Bot answers me,

    **Then** he displays a message informing me of the address, the start of Wikipedia article and its url and the here.com marked map.

2) User asks GrandPy Bot a place name that is not locatable by here.com.

    **Given** I am a user who is asking for a place address,

    **When** GrandPy Bot answers me,

    **Then** he displays a message informing me of incapacity to locate this place.

3) User asks GrandPy Bot a place name that is locatable by here.com but do not have a Wikipedia article.

    **Given** I am a user who is asking for a place address,

    **When** GrandPy Bot answers me,

    **Then** he displays a message informing me of the address and the here.com marked map.

INSTALLATION
============

Steps
-----

1) Download the project : use the "Code" (green button) and unzip the P7_GrandPyBot_DA-Python-master.zip file.
2) Python3 comes with Python Package Manager (pip) else you have to install it (https://pip.pypa.io/en/stable/installing/)

3) Set up a virtual environment :

    3.1) ``$ pip install pipx`` then ``$ pipx install pipenv``

    3.2) Create a virtual environment and Install project requirements (Pipfile) : ``$ pipenv install``

    3.3) Activate the virtual environment : ``$ pipenv shell``

4) Environment variables to be set :

    * DEBUG --> 1 for local/dev run | 0 for prod
    * HERE_API_KEY --> API key for here.com access

5) Run the code source main.py file : (UNIX) ``$ python ./main.py`` (DOS) ``$ py main.py``

6) Follow the http:// link given by Flask starting message on the terminal output (usually http://127.0.0.1:5000/) --> Web app interface is siplayed in the browser.


USAGE
=====
UI example
----------

.. image:: ./readme_images/Grandpy_Bot_example.jpg

API data
--------

**Mapping with here.com:**

here.com API response (see UI example above for the submitted and parsed user question) :

.. image:: ./readme_images/here.com_raw_json_resp.png

here.com API response parsed by the back_end and returned to the front-end :

.. image:: ./readme_images/here.com_parsed_json_resp.png

**Wikipedia infos :**

Wikipedia API response (see UI example above for the submitted and parsed user question) :

.. image:: ./readme_images/wikipedia_raw_json_resp.png

Wikipedia API response parsed by the back_end and returned to the front-end :

.. image:: ./readme_images/wikipedia_parsed_json_resp.png



.. |vPython badge| image:: https://img.shields.io/badge/Python-3.11-blue.svg
.. |vHTML badge| image:: https://img.shields.io/badge/HTML-5-orange.svg
.. |vCSS badge| image:: https://img.shields.io/badge/CSS-3-blue.svg
.. |JavaScript badge| image:: https://img.shields.io/badge/JavaScript-.-yellow.svg

.. |Status badge| image:: https://img.shields.io/badge/Status-Deploying-purple.svg
.. |UIlanguage badge| image:: https://img.shields.io/badge/UI-French-9cf.svg
