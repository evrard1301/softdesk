Comments
========

Create / Update a Comment
-------------------------

+--------+-----------------------------------------------+
| Create | POST /projects/{id}/issues/{id}/comments/     |
+--------+-----------------------------------------------+
| Update | PUT /projects/{id}/issues/{id}/comments/{id}/ |
+--------+-----------------------------------------------+

Allows a project collaborator to create a new issue comment or to update an existing one.

**description**
  The body of the comment.

**author**
  The author of the comment.

Delete a Comment
----------------

+--------------------------------------------------+
| DELETE /projects/{id}/issues/{id}/comments/{id}/ |
+--------------------------------------------------+

Allows a comment author to delete it.

List Comments
-------------

+------------------------------------------+
| GET /projects/{id}/issues/{id}/comments/ |
+------------------------------------------+

Allows a project collaborator to see the list of all the comments.

Show Comment
------------

+-----------------------------------------------+
| GET /projects/{id}/issues/{id}/comments/{id}/ |
+-----------------------------------------------+

Allows a project collaborator to see a given comment.
