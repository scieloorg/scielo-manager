Attempts API
===========

The main idea behind the Attempt Status API is to provide ways for `Balaio <https://github.com/scieloorg/balaio>`_. 
to change and retrieve the "changes status" of an **Article Package** .

.. note::

  It is important to notice that by now SciELO Manager is not responsible
  for managing Articles.
  This feature is currently `under development <https://github.com/scieloorg/SciELO-Manager/tree/articles>`_.

:Available data:

phase
  A string containg a phase from the submission process.

is_accomplished
  A boolean value to update the status.

changed_at
  Date when the status was registered and/or changed.


Updating a status to an existing attempt
----------------------------------------

Request::

  PUT /api/v1/attempt_status/{:id}/

warning::
  
  Not all users with a valid api token will be able to fetch a POST request, only those with the
  apropriate privileges.

  You must have a valid **attempt resource** to register a new status.

Parameters:

  {
    "is_accomplished": true,
    "changed_at": "2013-12-30T22:01:22"
  }