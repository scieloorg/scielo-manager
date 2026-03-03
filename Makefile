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
	@python3 $(MANAGE) test --settings=$(SETTINGS_TEST)

testfast:
	@python3 $(MANAGE) test --settings=$(SETTINGS_TEST) --failfast

dbsetup:
	@python3 $(MANAGE) migrate --settings=$(SETTINGS)

loaddata:
	@python3 $(MANAGE) loaddata $(FIXTURES_DIR)/groups.json --settings=$(SETTINGS)
	@python3 $(MANAGE) loaddata $(APP_PATH)/journalmanager/fixtures/use_licenses.json --settings=$(SETTINGS)
	@python3 $(MANAGE) loaddata $(FIXTURES_DIR)/subject_categories.json --settings=$(SETTINGS)
	@python3 $(MANAGE) loaddata $(FIXTURES_DIR)/study_area.json --settings=$(SETTINGS)
	@python3 $(MANAGE) sync_perms --settings=$(SETTINGS)

dbmigrate:
	@python3 $(MANAGE) migrate --settings=$(SETTINGS)

compilemessages:
	@python3 $(MANAGE) compilemessages --settings=$(SETTINGS)

compile: 
	@echo "Compiling all source files..."
	@cd $(APP_PATH) && python3 -m compileall .

setup: clean compile deps dbsetup dbmigrate loaddata compilemessages test 

upgrade: clean compile deps dbmigrate compilemessages
