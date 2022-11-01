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

.. code-block:: console

   cd src/softdesk
   ./manage.py migrate
   ./manage.py runserver
