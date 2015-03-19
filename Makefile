APP_PATH = scielomanager
MANAGE = $(APP_PATH)/manage.py
SETTINGS_TEST = scielomanager.settings_tests
SETTINGS = scielomanager.settings
FIXTURES_DIR = $(APP_PATH)/scielomanager/fixtures

deps:
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python $(MANAGE) test --settings=$(SETTINGS_TEST)

testfast: clean
	@python $(MANAGE) test --settings=$(SETTINGS_TEST) --failfast

dbsetup:
	@python $(MANAGE) syncdb --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/groups.json --settings=$(SETTINGS)

loaddata:
	@python $(MANAGE) loaddata $(APP_PATH)/journalmanager/fixtures/use_licenses.json --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/subject_categories.json --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/study_area.json --settings=$(SETTINGS)

dbmigrate:
	@python $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@cd $(APP_PATH) && python manage.py compilemessages --settings=$(SETTINGS)

setup: deps dbsetup dbmigrate loaddata compilemessages test refreshsecretkey

upgrade: deps dbmigrate compilemessages test
	@python $(MANAGE) sync_perms --settings=$(SETTINGS)

refreshsecretkey:
	@sed -e 's:^\(SECRET_KEY\).*$$:\1 = '" '`openssl rand -base64 32`' "':g' -i $(APP_PATH)/settings.py
