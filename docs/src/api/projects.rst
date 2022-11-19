Projects
========

Create Project
--------------
Allows an authenticated user to create a new project.

Endpoint
~~~~~~~~
POST /projects/

Parameters
~~~~~~~~~~
* **title** the title of the new project.
* **description** an optional description for the new project.
* **type** the type of the new project: "back-end", "front-end", "IOS" or "Android".

Returns
~~~~~~~
Returns the brand new project.

List Projects
-------------
Gives all the projects where the authentified user is a contributor.

Endpoint
~~~~~~~~
GET /projects/

Returns
~~~~~~~
Returns a list of projects.

Show Project
------------
Shows a project based on its ID.

Endpoint
~~~~~~~~
GET /projects/{id}/

Returns
~~~~~~~
Returns the project.

Update Project
--------------

Endpoint
~~~~~~~~
PUT /projects/{id}/

Parameters
~~~~~~~~~~

* **title** the new title of the project.
* **description** the new description of the project.
* **type** the new type of the project: "back-end", "front-end", "IOS" or "Android".

Returns
~~~~~~~
Returns the updated version of the project.
