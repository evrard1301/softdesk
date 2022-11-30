Comments
========

Create / Update a Comment
-------------------------

+--------+----------------------------------------------+
| Create | POST /projects/{id}/issues/{id}/comment/     |
+--------+----------------------------------------------+
| Update | PUT /projects/{id}/issues/{id}/comment/{id}/ |
+--------+----------------------------------------------+

Allows a project collaborator to create a new issue comment or to update an existing one.

**description**
  The body of the comment.

**author**
  The author of the comment.

**issue**
  The issue from where the comment belongs.

Delete a Comment
----------------

+------------------------------------------------+
| DELETE /projects/{id}/issues/{id}/comment/{id} |
+------------------------------------------------+

Allows a comment author to delete it.
