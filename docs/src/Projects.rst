Projects
========

Create / Update a Project
-------------------------

+--------+---------------------+
| Create | POST /projects/     |
+--------+---------------------+
| Update | PUT /projects/{id}/ |
+--------+---------------------+

Allows an authenticated user to create a new project or to update an existing one.

**title**
  The title of the project.

**description**
  The description of theproject.

**type**
  The type of the project: BACKEND, FRONTEND, ANDROID or IOS.

**author**
  The author of the project.


Delete a Project
----------------

+------------------------+
| DELETE /projects/{id}/ |
+------------------------+

Deletes a given project.

List Projects
-------------

+---------------+---------------------+
| Many projects | GET /projects/      |
+---------------+---------------------+
| One project   | GET /projects/{id}/ |
+---------------+---------------------+

List one or many  projects related to the authenticated user.
ie. The user is either a contributor, a supervisor or the author of the projects.
