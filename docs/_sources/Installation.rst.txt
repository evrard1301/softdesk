Installation
============

Install SoftDesk
----------------

To install the softdesk API follow those steps:

.. highlight:: bash
	    
1. Create a virtual environment
   
.. code-block:: bash
      
   python3 -m venv env

2. Activate the virtual environment

.. code-block:: bash

   source env/bin/activate

3. Install the dependencies

.. code-block:: bash

   pip install -r requirements.txt

And, voila !

Run SoftDesk
------------

To run the API, first go to the **softdesk** subdirectory.
Then, run the following commands:

.. code-block::

   ./manage.py migrate
   ./manage.py runserver

Optionnaly you can set the server address and port as shown in the
next code block.

.. code-block::

   ./manage.py runserver localhost:7575
