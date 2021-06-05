=====================
"GrandPy bot" project
=====================
**Searching for a spot address**

*****************
TABLE OF CONTENTS
*****************

1. `DESCRIPTION`_
    * `Features`_

2. `INSTALLATION`_
    * `Database installation`_
    * `Application`_
    * `Requirements`_

3. `USAGE`_
    * `json data examples`_
    * `Database`_
    * `OFF Search API query`_
        1) Default usage

DESCRIPTION
===========
This program asks user for choosing a food product in a local database and searches for an healthy alternative.
The user could back up each result in the local database to read it later.

Data in local database comes from Open Food Facts (OFF) french database (requested via the OFF search API). The retrieved json
data are parsed, reorganized and inserted in the local database.

Features
--------
I. A user could choose a food product in order to obtain an healthy substitution (Main menu choice 1-).

    I.1 Load data :
        I.1.1 Requests the OFF search API (see response.json_).

        I.1.2 Reorganized json responses (see valid_product.json_):

            * Keeps only products dictionaries and makes one list with all of them valid (= has the required fields).
            * Selects and translates categories (often in english in OFF search API responses).

        I.1.3 Inserts in the local database (see Installation section below for more information).

    I.2 User Interface (terminal) :

        I.2.1 Display numbered food products categories and ask user for choosing one. Then display numbered food
        products (belonging to the chosen category) and propose choosing one or going back to the categories choice.

        I.2.2 Compare the chosen food products to those having the same "compared_to_category" field to find a substitution
        (i.e with a better Nutri-Score).

        I.2.3 Display the substitution results : infos about the substituted food product and infos about the substitution food(s) found.

II. A user could back up a food product substitution in order to keep it in memory as a favorite.

        * User Interface (terminal) : when substitution results are displayed (see I.2.3), it proposes for recording in the database.

III. A user could get back his food product substitution favorites in order to read information without
repeating the research (Main menu choice 2-).

        * User Interface (terminal) : displays recorded substitution resumed results and it proposes for displaying more infos about one of them.

INSTALLATION
============

Database installation
---------------------

1) Install MySQL SGDB and then modify DB_PARAM dict (in config.py) to replace it with your database connection parameters.
2) Create the database by executing database_managers/pur_beurre_db_creation.sql (see Physical Data Model local_db_PDM_).

Application
-----------

1) Download the project : use the "Code" (green button) and unzip the P5_PurBeurre-Food-Substitution_DA-Python-master/
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


4) Install required libraries :
    * using the provided text file : $ pip install -r requirements.txt
    * OR install manually each Python package (see Requirements section below)

5) Run the code source main.py file : (UNIX) python ./main.py (DOS) py main.py

    ↳ Usage: [-h|--help] [-ld|--load_data] [-p|--page PAGE] [-v|--verbose]

Requirements
------------
|vPython badge|
|vHTML badge| |vCSS badge| |JavaScript badge|


Python libraries (see requirements.txt):

* ici copié+collé le contenu de requirements.txt

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

.. |vPython badge| image:: https://img.shields.io/badge/python-v3.8-blue.svg
.. |vHTML badge| image:: https://img.shields.io/badge/HTML-5-orange.svg
.. |vCSS badge| image:: https://img.shields.io/badge/CSS-3-blue.svg
.. |JavaScript badge| image:: https://img.shields.io/badge/JavaScript-.-yellow.svg
