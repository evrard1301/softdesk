Installation
============

Python libraries
----------------

.. code-block:: console
		
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt

Documentation
-------------

.. code-block:: console

   make html-docs

Running the API
===============

Initialize the API
------------------

.. code-block:: console

   cd src/softdesk
   ./manage.py migrate
   ./manage.py loaddata initial


Running the unit tests
----------------------

.. code-block:: console

   ./manage.py test

 
Running the server
------------------

.. code-block:: console

   ./manage.py runserver


Default Django Administrator
----------------------------

The default django administrator credentials are:

* **username:** *ocr-username*
* **password:** *ocr-password*.

