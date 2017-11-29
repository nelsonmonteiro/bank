def cached_method(func):
    """
    Cache result for an object to avoid to run the function multiple times.
    """
    def cache(*args, **kwargs):
        obj = args[0]
        temp_name = '_%s' % func.__name__
        if not hasattr(obj, temp_name):
            setattr(obj, '_%s' % func.__name__, func(*args, **kwargs))
        return getattr(obj, temp_name)
    return cache
