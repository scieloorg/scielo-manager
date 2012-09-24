APP_PATH = scielomanager
MANAGE = $(APP_PATH)/manage.py
SETTINGS_TEST = scielomanager.settings_tests
SETTINGS = scielomanager.settings
FIXTURES_DIR = $(APP_PATH)/fixtures

deps:
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python $(MANAGE) test journalmanager export --SETTINGS_TEST=$(SETTINGS_TEST)

dbsetup:
	@python $(MANAGE) syncdb --SETTINGS_TEST=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/groups.json --SETTINGS_TEST=$(SETTINGS)

dbmigrate:
	@python $(MANAGE) migrate --SETTINGS_TEST=$(SETTINGS)

compilemessages:
	@cd $(APP_PATH) && python manage.py compilemessages --SETTINGS_TEST=$(SETTINGS)

setup: deps dbsetup dbmigrate compilemessages test

upgrade: deps dbmigrate compilemessages test