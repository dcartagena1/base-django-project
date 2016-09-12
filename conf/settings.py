from conf.base_settings import *

# Project specific settings
INSTALLED_APPS += [
    # First the dependencies
    'apps.girocomercial',

    # Then apps from this branch
    'apps.conta',
]
