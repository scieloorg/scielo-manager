Attempts API
===========

The main idea behind the Attempt Status API is to provide ways for `Balaio <https://github.com/scieloorg/balaio>`_. 
to change and retrieve the "changes status" of an **Article Package** .

.. note::

  It is important to notice that by now SciELO Manager is not responsible
  for managing Articles.
  This feature is currently `under development <https://github.com/scieloorg/SciELO-Manager/tree/articles>`_.


:Available data:

{"attempt": "/api/v1/attempts/2/", "accomplished": "upload"}

attempt
  The resource of the related attempt in the API.

accomplished
  A string containing the change status.

created_at
  Date when the status was registered.


Register a status to an existing attempt
----------------------------------------

Request::

  POST /api/v1/attempt_status

warning::
  
  Not all users with a valid api token will be able to fetch a POST request, only those with the
  apropriate privileges.

  You must have a valid **attempt resource** to register a new status.

Parameters:

  {
    "attempt": "/api/v1/attempts/2/",
    "accomplished": "integrit_validation"
  }