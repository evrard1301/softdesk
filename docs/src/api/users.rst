Users
=====

Add Contributor
---------------

Add a new contributor to a given project.

Endpoint
~~~~~~~~

POST /projects/{id}/users/

Parameters
~~~~~~~~~~

* **user_id** the ID of the user to add as contributor.

List Contributors
-----------------

Lists all the contributors of a project.

Endpoint
~~~~~~~~

GET /projects/{id}/users/

Returns
~~~~~~~

All the contributors of the given project.

Delete Contributor
------------------

Delete a contributor of a project. The user still exists but he/she
doesn't belongs to the given project anymore

Endpoint
~~~~~~~~

DELETE /projects/{id}/users/{id}

Returns
~~~~~~~

The contributor just removed.
