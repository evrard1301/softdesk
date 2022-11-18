Users
=====

Add Contributor
---------------
Grant a user into a contributor of a project.

Endpoint
~~~~~~~~
POST /projects/{id}/users/

Parameters
~~~~~~~~~~
* **user_id** the ID of the user to grant.

List Contributors
-----------------
Given a project, returns a list of all its contributors.

Endpoint
~~~~~~~~
GET /projects/{id}/users/

Remove Contributor
------------------
Remove a contributor of a given project.

Endpoint
~~~~~~~~
DELETE /projects/{id}/users/

Parameters
~~~~~~~~~~
* **user_id** the ID of the user to remove.
