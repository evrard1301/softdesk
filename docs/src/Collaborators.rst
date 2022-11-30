Collaborators
=============

Assign a Collaborator
---------------------

 +----------------------------+
 | POST /projects/{id}/users/ |
 +----------------------------+

Assigns a user to a project as an author, a contributor or a
supervisor.

**user**
  The ID of the user to assign.

**role**
  The role (ie. the status) of the user for this project.
  Either AUTHOR, CONTRIBUTOR or SUPERVISOR.

Delete a Collaborator
---------------------

 +----------------------------------+
 | DELETE /projects/{id}/users/{id} |
 +----------------------------------+

Removes a user from a given project.

List Collaborators
------------------

 +---------------------------+
 | GET /projects/{id}/users/ |
 +---------------------------+

Returns a list of all the collaborators of a given project.
