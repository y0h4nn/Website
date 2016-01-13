import redis
from django.http import HttpResponse
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


r = redis.StrictRedis(host='localhost', port=6379, db=0)


def invalid_cache(key):
    r.set(key, 1)


def invalid_fragment_cache(fragment_name, *variables):
    cache_key = make_template_fragment_key(fragment_name, vary_on=variables)
    cache.delete(cache_key)


def cache_unless(key, methods=["OPTIONS", "GET"]):
    def outer_wrapper(func):
        def wrapper(request, *args, **kwargs):
            if request.method in methods:
                name = "%s_%s" % (func.__name__, request.method)
                if r.get(key) is not None:
                    r.delete(key)
                    for method in methods:
                         r.delete("%s_%s" % (func.__name__, method))

                cached = r.get(name)
                if cached is None:
                    res = func(request, *args, **kwargs)
                    r.set(name, res.content)
                    return res
                return HttpResponse(cached.decode())
            return func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper

