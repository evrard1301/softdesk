Authentication
==============

Sign Up
-------
Allows a new user to create an account.

Endpoint
~~~~~~~~
POST /signup/

Parameters
~~~~~~~~~~
* **username** the username of the new user.
* **first_name** the first name of the new user.
* **last_name** the last name of the new user.
* **password** the new account password.
* **email** the new account email address.

Log In
------
Allows a registrated user to log in.
Returns a valid JSON Web Token on success.

Endpoint
~~~~~~~~
POST /login/

Parameters
~~~~~~~~~~
* **username** the account username.
* **password** the account password.
