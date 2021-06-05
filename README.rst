=====================
"GrandPy bot" project
=====================
**Searching for a spot address**

|Status badge| |UIlanguage badge|

*****************
TABLE OF CONTENTS
*****************

1. `DESCRIPTION`_
    * `Summary`_
    * `Feature and scenario`_

2. `INSTALLATION`_
    * `Steps`_
    * `Required libraries`_

3. `USAGE`_
    * `json data examples`_
    * `Database`_
    * `OFF Search API query`_
        1) Default usage

DESCRIPTION
===========

Summary
-------
This Web application suggests questioning for locating a place to user by entering a question in an text input field and submit it.

A robot (GrandPy Bot) parses the text input and requests here.com API to obtain and display the place address and a map marked with it.
It also requests Wikipedia API to obtain an article (if it exists) about the place and display the url and the start of it.

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

    NB: the symbol $ flags the commands prompt

    * UNIX operating system :
        3.1) Install the Python module : $ pip install venv

        3.2) Navigate to the project main directory using command prompt : $ cd .....

        3.3) Create a virtual environment : $ python -m venv name_of_your_virtual_env

        3.4) Activate the virtual environment : $ source name_of_your_virtual_env/bin/activate

    * DOS operating system :

        3.1) Install the Python module : $ pip install venv

        3.2) Navigate to the project main directory using command prompt : $ cd .....

        3.3) Create a virtual environment : $ py -m venv name_of_your_virtual_env

        3.4) Activate the virtual environment : $ .\name_of_your_virtual_env\Scripts\activate


4) Install required libraries : see the Required libraries section below.

5) Set your personnel parameters for here.com API access :
    * Get a free apikey by creating a "Freemium" account : https://developer.here.com/sign-up?create=Freemium-Basic&keepState=true&step=account
    * Copy + Paste your apikey as a string value replacing the '******' of HERE_API_KEY constant variable in config.py file.

6) Run the code source main.py file : (UNIX) python ./main.py (DOS) py main.py

7) Click on the http:// link given by Flask starting message on the terminal output (usually http://127.0.0.1:5000/) to display interface in your browser.

Required libraries
------------------
|vPython badge|
|vHTML badge| |vCSS badge| |JavaScript badge|


Python libraries to install in your virtual environment : $ pip install -r requirements.txt


USAGE
=====
json data examples
------------------
**OFF search API response structure :**

.. _response.json:
.. image:: ./ImagesReadme/OFF_search_API_response_1_product.png

|

**Final list of valid products dict structure :**

(after reorganization, see feature I.1.2)

.. _valid_product.json:
.. image:: ./ImagesReadme/1_valid_product.png

Database
--------

**Each json field (see picture above) corresponds to one in the local database:**

see local_db_PDM_ below

Table 'food' :

* "_id" = barcode
* "product_name" = name
* "nutriscore_grade" = Nutri-Score
* "url" = url
* "quantity" = quantity (optional field, used to specify some food product having same name but different barcode because of different quantity).
* "compared_to_category" = compared_to_category (unique keyword used to find a relevant substitution food).

Table 'category' :

* "categories_tags" = list where each element is a row in the table (name field)


Table 'store' :

* "stores_tags" = list where each element is a row in the table (name field)

**Local database :**

.. _local_db_PDM:
.. image:: ./ImagesReadme/local_db_schema.png

.. |vPython badge| image:: https://img.shields.io/badge/Python-3.8-blue.svg
.. |vHTML badge| image:: https://img.shields.io/badge/HTML-5-orange.svg
.. |vCSS badge| image:: https://img.shields.io/badge/CSS-3-blue.svg
.. |JavaScript badge| image:: https://img.shields.io/badge/JavaScript-.-yellow.svg

.. |Status badge| image:: https://img.shields.io/badge/Status-Development-orange.svg
.. |UIlanguage badge| image:: https://img.shields.io/badge/UI-French-9cf.svg
