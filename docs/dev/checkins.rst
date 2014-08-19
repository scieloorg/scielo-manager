SciELO Manager Checkin's workflow
=================================

Description of Checkin's workflow developed in SciELO Manager, the steps, actions, responsibilities and results.


Prelude/Disclaimer:
-------------------

This document describes only the workflow of the Checkins, and user's interactions, all further actions related with the module Articles In Submission, exceeds the scope of this docs, such as XML annotations, Stylecheckers, Tickets, etc.
Is assumed that you know how is the interaction with Balaio, how to upload a package, and also knows about automated validations of the packages, structure and formats of the packages, and everything related with required files and formats to be included in the process of package submission.


Introduction:
-------------

Every valid package uploaded to Balaio, will generate a Checkin, associated with an article, and those related notices with the results of automatic validations.
The Checkin, is an attempt of submission of an article, to be incorporated in the SciELO Manager.
All operations (made or not by a user) will be logged, to keep track of Checkin's changes. And this logs are accessible to user (referred as Checkin History [2]_).
Also important changes will trigger emails to notify others users [1]_ related with the submission of the article.


Users, Permissions, Groups, and Roles:
--------------------------------------

We defined 3 differents groups of users that reach in differents part of the workflow's operations.
To manipulate a Checkin, is mandatory to be part of at least one this Groups.

  * **Producer**:

    Is the lower level, users in this group represents a user that submit (or want to keep track of a submited) package to see their evolution in the workflow.

  * **QAL1**:

    Represents a user with the same capabilities of a **Producer** user, and also can do a first review (**Editorial Review**) of the package.

  * **QAL2**:

    Represents a user with the same capabilities of a **QAL1** user, and also can do a final review (**SciELO Review**) of the package, then accepts, and triggers the checkout process.

For simplicity, sometimes a "Producer" (or "QAL1" or "QAL2") user is mentioned, when the meaning is to refers to a user that belongs to this group.


Checkin Status:
---------------

Along the submission process the Checkin will pass between a few stages, each one is represented by a status, and this status together with the users permissions will determine the possible actions to do.

  * **Pending**:

    Is the lower level, users in this group represents a user that submit (or want keep track of a submited) package to see their evolution in the workflow.

  * **Expired**:

    If a **pending** Checkin remains unchanged, for a while (normally more than 7 days), the Checkin will be expired, and unaccessible to the user.

  * **Review**:

    The Checkin with this state, represent a Checkin ready to be reviewed by a QAL1 user (doing a **Editorial Review**), and also is possible to be reviewed by a QAL2 user (doing a **SciELO Review**), without specific order of events is required.

  * **Accepted**:

    Right after a Checkins got both reviews (**Editorial Review** and **SciELO Review**) the Checkin can be switched to this status, which means that everything is ok to be checkout.

  * **Scheduled to Checkout**:

    Right after a Checkin was accepted, can be switched this status, to be collected by a system process, and proceed to checkout.

  * **Checkout Confirmed**:

    When the Checkin was processed, and checkout process was ok, the Checkin will be changed to this status.


Checkin Actions:
----------------

To switch between the previous status, the SciELO Manager offer differents actions, for each we present the pre conditions, and post conditions, and a brief description.

    * **Send to review**:
        A Checkin with status **pending** will change the status to  **review**, expecting both reviews.

        * *Pre*: Checkin's status is **pending**.
        * *Pre*: Checkin's error level must be "ok" or "warning".
        * *Pre*: The article related to the Checkin, must not be accepted previously.
        * *Pre*: User must be active, and belongs to: **Producer**, **QAL1** or **QAL2** groups.

        * *Post*: Checkin's status will change to: **review**.
        * *Post*: If Checkin has filled the field: ``submitted_by``, users will be notified via email [1]_.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.

    * **Editorial Review**:
        A Checkin with status **review** could be marked as "Editorial Reviewed" by the user that submit this action.

        * *Pre*: Checkin's status is **review**.
        * *Pre*: Checkin's error level must be "ok" or "warning".
        * *Pre*: User must be active, and belongs to: **QAL1** or **QAL2** groups.
        * *Pre*: The article related to the Checkin, must not be accepted previously.

        * *Post*: Checkin's status will remains as: **review**.
        * *Post*: Checkin will store informations about the review, such as the user that made the review, and the date.
        * *Post*: If Checkin has filled the field: ``submitted_by``, users will be notified via email [1]_.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.

    * **SciELO Review**:
        A Checkin with status **review** could be marked as "SciELO Reviewed" by the user that submit this action.
        Usually, the user make SciELO review, after the *Editorial review*, but no specific order is required.

        * *Pre*: Checkin's status is **review**.
        * *Pre*: Checkin's error level must be "ok" or "warning".
        * *Pre*: User must be active, and belongs to: **QAL2** group.
        * *Pre*: The article related to the Checkin, must not be accepted previously.

        * *Post*: Checkin's status will remains as: **review**
        * *Post*: Checkin will store informations about the review, such as the user that made the review, and the date.
        * *Post*: If Checkin has filled the field: ``submitted_by``, users will be notified via email [1]_.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.
        * *Post*: If the Checkin is fully reviewed [3]_, then the system will automatically try to run **Accept** actions, and furhter **Send to checkout** to simplify the future steps to the user.

    * **Accept**:
        If a Checkin was fully reviewed [3]_, with this action will be switched to **accepted** status, which means that will be ready to be checked out.

        * *Pre*: Checkin's status is **review**, and **Editorial reviewed** and **SciELO reviewed**.
        * *Pre*: User must be active, and belongs to: **QAL2** group.
        * *Pre*: The article related to the Checkin, must not be accepted previously.

        * *Post*: Checkin's status will be changed to: **accepted**.
        * *Post*: Checkin will store informations about the acceptance, such as the user that made the action, and the date.
        * *Post*: If Checkin has filled the field: ``submitted_by``, users will be notified via email [1]_.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.
        * *Post*: If the Checkin is accepted, then the system will automatically try to run **Send to checkout** action, to simplify the future steps to the user.

    * **Send to checkout**:
        If a Checkin was accepted, with this actions will switch status to **Scheduled to Checkout**, and then will be ready to be processed by a system task, that will collect the Checkins with this status, and proceed to checkout.

        * *Pre*: the Checkin's status is **accepted**.
        * *Pre*: User must be active, and belongs to: **QAL2** group.
        * *Pre*: The article related to the Checkin, must not be accepted previously.

        * *Post*: Checkin's status will remains as: **Scheduled to Checkout**.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.


**Checkin Checkout**:

    All Checkins with status: **Scheduled to Checkout** will be collected by a system task, and processed to make a checkout.
    No user action are required

        * *Pre*: the Checkin's status is **Scheduled to Checkout**.

        * *Post*: the Checkin's status will be set to: **Checkout Confirmed**.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.


**Rejecting a Checkin**:

    * **Reject**:
        At review stages, if the reviewer user think that something is wrong, could reject the Checkin, submitting also a required explanation about the rejection.

        * *Pre*: the Checkin's status is **pending**, or **review** (even **Editorial reviewed** or **SciELO reviewed**).
        * *Pre*: The article related to the Checkin, must not be accepted previously.
        * *Pre*: User must be active, and belongs to: **Producer**, **QAL1** or **QAL2** groups.

        * *Post*: Checkin's status will be changed to: **rejected**.
        * *Post*: Checkin will store informations about the reject, such as the user that made the action, and the date.
        * *Post*: If Checkin has filled the field: ``submitted_by``, users will be notified via email [1]_.
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.


**Checkin Expiration**:

    Each *Pending Checkin* that remains in this status for 7 days [4]_, is assumed as expirable, which means that the Checkin is "abandoned".
    There is a system task that collect all expirables Checkins [5]_, and proceed with process and change the status to: **expired**.
    Every time the Checkin was sent to review, or leave the **pending** status, when come back to **pending** status again, the expiration date will be re-calculated, to the next 7th day.
    No user action is required.

        * *Pre*: the Checkin's status is **pending**.
        * *Pre*: the Checkin's field: ``expiration_date`` is equal or previous than current date.

        * *Post*: the Checkin's status will be set to: **expired**
        * *Post*: A (history) log entry will be created, to inform about this change [2]_.


.. [1] ``submitted_by`` field refers to a valid user, if he belongs to a Team, all members of the team will be notified about the Checkin changes.

.. [2] history logs will store: the entry creation date, the user that made the action, the status of the Checkin, a brief description, and a reference to the related Checkin.

.. [3] A fully reviewed Checkin means that the Checkin was **Editorial Reviewed** and **SciELO Reviewed** successfully.

.. [4] The period is 7 days, and is configurable.

.. [5] Currently, the task that collect all expirable checkin, run daily at 00:00hs. Please refer to task docs for more info.



Workflows:
----------

1. Simple view:

    .. image:: ../images/workflow_simple.png

2. Detailed view:

    .. image:: ../images/workflow_simple.png

3. Transitions from status: Pending

    .. image:: ../images/from_pending.png

4. Transitions from status: Review

    .. image:: ../images/from_review.png

5. Transitions from status: Accepted

    .. image:: ../images/from_accepted.png
