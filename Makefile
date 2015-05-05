APP_PATH = scielomanager
MANAGE = $(APP_PATH)/manage.py
SETTINGS_TEST = scielomanager.settings_tests
SETTINGS = scielomanager.settings
FIXTURES_DIR = $(APP_PATH)/scielomanager/fixtures

deps:
	@pip install -r requirements.txt

clean:
	@echo "Removing all .pyc files..."
	@find . -name "*.pyc" -delete

test: 
	@python $(MANAGE) test --settings=$(SETTINGS_TEST)

testfast:
	@python $(MANAGE) test --settings=$(SETTINGS_TEST) --failfast

dbsetup:
	@python $(MANAGE) syncdb --settings=$(SETTINGS)

loaddata:
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/groups.json --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(APP_PATH)/journalmanager/fixtures/use_licenses.json --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/subject_categories.json --settings=$(SETTINGS)
	@python $(MANAGE) loaddata $(FIXTURES_DIR)/study_area.json --settings=$(SETTINGS)
	@python $(MANAGE) sync_perms --settings=$(SETTINGS)

dbmigrate:
	@python $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@python $(MANAGE) compilemessages --settings=$(SETTINGS)

compile: 
	@echo "Compiling all source files..."
	@cd $(APP_PATH) && for PYMOD in $$(find . -name '*.py'); do python -m compileall $$PYMOD; done

setup: clean compile deps dbsetup dbmigrate loaddata compilemessages test 

upgrade: clean compile deps dbmigrate compilemessages
