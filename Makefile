APP_PATH = scielomanager
MANAGE = $(APP_PATH)/manage.py
SETTINGS = scielomanager.settings
FIXTURES_DIR = $(APP_PATH)/fixtures

deps:
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python $(MANAGE) test journalmanager --settings=$(SETTINGS)
	@python $(MANAGE) test export --settings=$(SETTINGS)

dbsetup:
	@python $(MANAGE) syncdb --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/groups.json --settings=$(SETTINGS)

dbmigrate:
	@python $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@cd $(APP_PATH) && python manage.py compilemessages --settings=$(SETTINGS)

setup: deps dbsetup dbmigrate compilemessages test

upgrade: deps dbmigrate compilemessages test