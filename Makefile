APP_PATH = scielomanager
MANAGE = $(APP_PATH)/manage.py
SETTINGS_TEST = scielomanager.settings_tests
SETTINGS = scielomanager.settings
FIXTURES_DIR = $(APP_PATH)/fixtures
APPS_TO_TEST = journalmanager export api accounts maintenancewindow

deps:
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python $(MANAGE) test $(APPS_TO_TEST) --settings=$(SETTINGS_TEST)

dbsetup:
	@python $(MANAGE) syncdb --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/groups.json --settings=$(SETTINGS)

loaddata:
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/subject_categories.json --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/study_area.json --settings=$(SETTINGS)

dbmigrate:
	@python $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@cd $(APP_PATH) && python manage.py compilemessages --settings=$(SETTINGS)

setup: deps dbsetup dbmigrate loaddata compilemessages test

upgrade: deps dbmigrate compilemessages test
	@python $(MANAGE) sync_perms --settings=$(SETTINGS)
