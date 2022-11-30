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
