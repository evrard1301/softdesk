Issues
======

Create / Update an Issue
-------------------------

+--------+----------------------------------+
| Create | POST /projects/{id}/issues/      |
+--------+----------------------------------+
| Update | PUT /projects/{id}/issues/{id}/  |
+--------+----------------------------------+

Allows a project collaborator to create a new issue or to update an existing one.

**title**
  The title of the issue.

**description**
  The description of the issue.

**tag**
  A tag describing the issue: BUG, TASK or IMPROVEMENT.

**priority**
  An integer representing the priority of the project.
  
**project**
  The project of the issue.
  
**status**
  The status of the issue: OPEN or CLOSED.
  
**author**
  The ID of the author user.
  
**assignee**
  The ID of the assignee user.

List Issues
-----------

+----------------------------+
| GET /projects/{id}/issues/ |
+----------------------------+

Returns the list of the issues of a given project.

Delete an Issue
---------------

+-----------------------------------+
| DELETE /projects/{id}/issues/{id} |
+-----------------------------------+

Deletes an issue of a given project.
