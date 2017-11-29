from django.utils.html import strip_tags
import traceback
import sys


class ProcessExceptionMiddleware(object):
    """
    Print errors on terminal. Useful when error can't be shown on client side
    """
    def process_response(self, request, response):
        if response.status_code > 299 or response.status_code < 200:
            print strip_tags(response)
            print traceback.print_exc()
            print '\n'.join(traceback.format_exception(*sys.exc_info()))
        return response
