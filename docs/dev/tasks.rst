SciELO Manager Tasks
====================

Description of tasks developed in SciELO Manager and their responsibilities

List all tasks:
---------------

1. **scielomanager.send_mail(self, subject, content, to_list, html=True)**

  Responsible to send an email, based in the args.

  * **Periodic task**: No.
  * **Args**:

    * ``subject``: email subject.
    * ``content``: email message.
    * ``to_list``: list of recipients of the email.
    * ``html``: boolean indicates if email body will be rendered as html. Default value is ``True``

  * **Output**: None
  * **Retry when**: occurs an error when calling send method

Default Retrying Policy:
------------------------

By default all task are configured to be re-executed 3 more times, with a delay of 3 minutes between each retry.
