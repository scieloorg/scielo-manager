import os
import glob


SCIELOMANAGER_SETTINGS_FILE = os.environ.get('SCIELOMANAGER_SETTINGS_FILE', None)


conf_files_path = os.path.join(os.path.dirname(__file__), 'settings', '*.conf')
conffiles = glob.glob(conf_files_path)
conffiles.sort()

for f in conffiles:
    execfile(os.path.abspath(f))

if SCIELOMANAGER_SETTINGS_FILE:
    execfile(SCIELOMANAGER_SETTINGS_FILE)

