from .project import *

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

# Output email on the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


# set up django-devserver if installed
try:
    import devserver
    INSTALLED_APPS += (
        'devserver',
    )
    # more details at https://github.com/dcramer/django-devserver#configuration
    DEVSERVER_DEFAULT_ADDR = '0.0.0.0'
    DEVSERVER_DEFAULT_PORT = '8000'
    DEVSERVER_AUTO_PROFILE = False  # use decorated functions
    DEVSERVER_TRUNCATE_SQL = True  # squash verbose output, show from/where
    DEVSERVER_MODULES = (
        # uncomment if you want to show every SQL executed
        # 'devserver.modules.sql.SQLRealTimeModule',
        # show sql query summary
        'devserver.modules.sql.SQLSummaryModule',
        # Total time to render a request
        'devserver.modules.profile.ProfileSummaryModule',

        # Modules not enabled by default
        # 'devserver.modules.ajax.AjaxDumpModule',
        # 'devserver.modules.profile.MemoryUseModule',
        # 'devserver.modules.cache.CacheSummaryModule',
        # see documentation for line profile decorator examples
        # 'devserver.modules.profile.LineProfilerModule',
        # show django session information
        # 'devserver.modules.request.SessionInfoModule',
    )
except ImportError:
    pass