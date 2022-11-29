Authentication
==============

Create an account
-----------------

+---------------+
| POST /signup/ |
+---------------+

Allows a new user to create an account.

**username**
  The username of the new user.

**first_name**
  The first name of the new user.
  
**last_name**
  The last name of the new user.

**email**
  The email address of the new user.
  
**password**
  The password of the new user.

Returns code 201 on success, 400 otherwise.
