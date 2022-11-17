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

List Projects
--------------
Allows an authenticated user to see a list of its projects.

Endpoint
~~~~~~~~
GET /projects/

Parameters
~~~~~~~~~~
None
