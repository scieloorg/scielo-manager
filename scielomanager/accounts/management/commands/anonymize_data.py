# coding: utf-8
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Q

def display_users(users_list):
    print "-" * 80
    print "| pk | username | first_name | last_name | email |"
    for user in users_list:
        print "| %s | %s | %s | %s | %s |" % (user.pk, user.username, user.first_name, user.last_name, user.email)
    print "-" * 80
    print "total: %s users" % users_list.count()
    print "-" * 80


class Command(BaseCommand):
    help = 'replace sensible data to be anonymized, such as first_name, last_name, email, api tokens, etc'

    def handle(self, *args, **options):
        print "#" * 80
        print "# THIS COMMAND WILL MODIFY USER DATA, AND SHOULD AFFECT THE LOGIN CREDENTIALS! #"
        print "# ----------- PLEASE BE SURE YOU HAVE A BACKUP TO AVOID DATA LOSS ------------ #"
        print "#" * 80
        prompt_backup = raw_input('the database has a back up? [y/N]: ')
        if prompt_backup.lower() == 'y':
            users = User.objects.all()
            print "Found %s users!" % users.count()
            prompt_show_all_users = raw_input('want to list all these users? [y/N]: ')
            if prompt_show_all_users.lower() == 'y':
                display_users(users)

            # exclude non-scielo users
            non_scielo_users = users.exclude(email__endswith="@scielo.org")
            print "Found %s NON-scielo users!" % non_scielo_users.count()
            prompt_show_non_scielo_users = raw_input('want to list all these users? [y/N]: ')
            if prompt_show_non_scielo_users.lower() == 'y':
                display_users(non_scielo_users)

            # lookup to know if exists particular users to be excludes, such as: QAL1, QAL2, Produtor, etc
            has_special_users = non_scielo_users.filter(
                Q(first_name__iexact="Produtor") | Q(first_name__iexact="QAL1") | Q(first_name__iexact="QAL2")
            ).exists()

            if has_special_users:
                prompt_to_exclude_special_users = raw_input(
                    'Found at least one special user (QAL1 or QAL2 or Produtor). Do you want to ignore this users from modifications? [y/N]: '
                )
                if prompt_to_exclude_special_users.lower() == 'y':
                    non_scielo_users = non_scielo_users.exclude(
                        Q(first_name__iexact="Produtor") | Q(first_name__iexact="QAL1") | Q(first_name__iexact="QAL2")
                    )
                    print "Now the list of NON-scielo users to be modified has %s users" % non_scielo_users.count()
                    prompt_show_non_scielo_users = raw_input('want to list all these users? [y/N]: ')
                    if prompt_show_non_scielo_users.lower() == 'y':
                        display_users(non_scielo_users)

            print "#" * 80
            print "# NOW WILL MODIFY USER DATA! #"
            print "# user.username will be set to user_<user.pk> #"
            print "# user.first_name will be set to user_fn_<user.pk> #"
            print "# user.last_name will be set to user_ln_<user.pk> #"
            print "# user.email will be set to user_<user.pk>@example.com #"
            print "# user.password will be set to 'test.scielo' [hashed] #"
            print "# user.api_key will be regenerated with a random uuid using tastypie.models > ApiKey > generate_key #"
            print "# ----------- BE SURE YOU HAVE A BACKUP TO AVOID DATA LOSS ------------ #"
            print "#" * 80
            prompt_confirm_modify = raw_input('Are you sure? the process CAN NOT BE UNDONE [y/N]: ')
            if prompt_confirm_modify.lower() == 'y':
                print "Updating users ... (hold on, may take a while) ..."
                for user in non_scielo_users:
                    user.username = "user_%s" % user.pk
                    user.first_name = "user_fn_%s" % user.pk
                    user.last_name = "user_ln_%s" % user.pk
                    user.email = "user_%s@example.com" % user.pk
                    user.set_password('test.scielo')
                    # save new user field
                    user.save()
                    # generate a new api_key
                    user.api_key.key = None
                    user.api_key.save()
                # show updated user info
                display_users(non_scielo_users)
                print "done!"
            else:
                print "Nothing to do here! NON-scielo users were NOT changed!"
        else:
            print "Nothing to do here! Go and make a backup."
