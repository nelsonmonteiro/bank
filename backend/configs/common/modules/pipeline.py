STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'STYLESHEETS': {
        'theme': {
            'source_filenames': [
              'style/theme.scss',
            ],
            'output_filename': 'style/theme.css',
            'variant': 'datauri',
        },
    },
    'JAVASCRIPT': {
        'helpers': {
            'source_filenames': (
              'js/helpers.js',
            ),
            'output_filename': 'js/helpers.js',
        }
    },
    'COMPILERS': [
        'pipeline.compilers.sass.SASSCompiler',
    ],
    'SASS_BINARY': 'sass',
    'MIMETYPES': (
        (b'text/coffeescript', '.coffee'),
        (b'text/less', '.less'),
        (b'text/javascript', '.js'),
        (b'text/css', '.css'),
        (b'text/x-scss', '.scss')
    ),
}


### AMAZON ####################################################################
STATIC_FILES_BUCKET = ''
STATIC_FILES_DOMAIN = ''
DEFAULT_FILES_BUCKET = ''
DEFAULT_FILES_DOMAIN = ''

