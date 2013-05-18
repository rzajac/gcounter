# --- Main Configuration ---

# Project paths
PROJECT_ROOT=.

# Test suite config
TMOD?=tests
TMET?=

# AppEngine dev server config
GAE_SDK=/usr/local/google_appengine

# --- Targets ---

test:
	${PROJECT_ROOT}/tests/testrunner.py ${GAE_SDK} ${TMOD} ${TMET}

remove_pyc:
	@find ${PROJECT_ROOT} -name '*.pyc' -exec rm -f {} \;

clean: remove_pyc
