Problems
========

Create Issues
-------------
Creates a new project issue.

Endpoint
~~~~~~~~
POST /projects/{id}/issues/

Parameters
~~~~~~~~~~
* **title** the title of the issue.
* **desc** a short description.
* **tag** *bug*, *task* or *improvement* tag.
* **priority** the priority of the issue.
* **project** the id of the  project the issue refers to.
* **status** either *opened* or *closed*.
* **author** id of the author of the issue.
* **assignee** id of the user assigned to the issue.
  
Returns
~~~~~~~
Returns the created issue.

List Issues
-----------
Gives the list of all  the issues of a given project.

Endpoint
~~~~~~~~
GET /projects/{id}/issues/

Returns
~~~~~~~
Returns the list of all the issues.

Update Issue
-------------
Update an existing project.

Endpoint
~~~~~~~~
PUT /projects/{id}/issues/{i}/

Parameters
~~~~~~~~~~
* **title** the title of the issue.
* **desc** a short description.
* **tag** *bug*, *task* or *improvement* tag.
* **priority** the priority of the issue.
* **project** the id of the  project the issue refers to.
* **status** either *opened* or *closed*.
* **author** id of the author of the issue.
* **assignee** id of the user assigned to the issue.
