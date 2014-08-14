SciELO Manager Tasks
====================

List of tasks developed in SciELO Manager and their responsibilities

List all tasks
-----------------

1. **articletrack.do_expires_checkin(checkin)**

  Responsible to expire checkins.

    Condition for expiration:
      checkin.status = pending

      checkin.expiration_at = Null

      checkin.expiration_at = Null

      checkin.expiration_at <= current date

    OBS.: expiration_at is insert by date of creation + 7 days

2. **articletrack.process_expirable_checkins() (every day at 12:00hs)**

  uses **articletrack.do_expires_checkin(checkin)** to expire checkin eligible for expiration.

  OBS.: this task is registered in the scheduler of celery (celery beat)

3. **scielomanager.send_mail(self, subject, content, to_list, html=True)**

  Send e-mail consider a list of e-mail.


All tasks are configured to re-excuted in 3 times in a delta time of 3 minutes
