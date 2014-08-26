SciELO Manager Tasks
====================

Description of tasks developed in SciELO Manager and their responsibilities

List all tasks:
---------------

1. **articletrack.tasks.do_expires_checkin(checkin)**

  Responsible to expire a single checkin.

  * **Periodic task**: No.
  * **Args**:

    * ``checkin``: a checkin object, normally this checkin comply with conditions to be expired (``checkin.is_expirable == True``).

  * **Output**: None.
  * **Retry when**: Can't contact Balaio, or RPC call fails.

  The task will contact Balaio's RPC API and requests to expire the checkin, if this call succeed, then change the checkin status to ``expired``,  by calling : ``checkin.do_expires()``.

2. **articletrack.tasks.process_expirable_checkins()**

  Responsible to collect all expirable checkins, and enqueue checkins to be processed by ``articletrack.tasks.do_expires_checkin``.

  * **Periodic task**: Yes (registered in Celery Beat to run daily at 00:00 hs).
  * **Args**: None.
  * **Output**: None.
  * **Retry**: No, all unprocessed checkins, will be collected the next run.

  The task filters all expirable checkins (all checkins with status ``pending`` and with any expiration date), for each checkin, if comply with: ``checkin.is_expirable == True`` will be processed.
  Every matching checkin, will have expiration date previous or equals than current date, then will be enqueued to be processed by the task: **articletrack.do_expires_checkin(...)** that effectively expires the checkins.

3. **scielomanager.send_mail(self, subject, content, to_list, html=True)**

  Responsible to send an email, based in the args.

  * **Periodic task**: No.
  * **Args**:

    * ``subject``: email subject.
    * ``content``: email message.
    * ``to_list``: list of recipients of the email.
    * ``html``: boolean indicates if email body will be rendered as html. Default value is ``True``

  * **Output**: None
  * **Retry when**: occurs an error when calling send method

4. **articletrack.tasks.do_proceed_to_checkout(checkin_id)**

  Responsible to pick a single checkin, verify that is scheduled to be checked out, contact Balaio RPC API, and proceed with checkout process.

  * **Periodic task**: No.
  * **Args**:

    * ``checkin_id``: the id of the checkin to be processed.

  * **Output**: None.
  * **Retry when**: Can't contact Balaio, or RPC call fails.

  The task retrieves the checkin by the id, verifies if comply with requirements to be schedulede to be checked out, then contact Balaio RPC API, and requests to proceed to checkout, then if all succeeded, change the checkin status to ``checkout_confirmed`` by calling: ``checkin.do_confirm_checkout()``

5. **articletrack.tasks.process_checkins_scheduled_to_checkout**

  Responsible to collect all the checkins scheduled to be checked out (``checkin.status == 'checkout_scheduled'``), and enqueue checkins to be processed by ``articletrack.tasks.do_proceed_to_checkout``.

  * **Periodic task**: Yes (registered in Celery Beat to run hourly).
  * **Args**: None.
  * **Output**: None.
  * **Retry**: No, all unprocessed checkins, will be collected the next run.


Default Retrying Policy:
------------------------

By default all task are configured to be re-executed 3 more times, with a delay of 3 minutes between each retry.
