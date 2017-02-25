import os
from django.http import HttpResponse, Http404


# https://github.com/dmathieu/sabayon#python-django
def acme_challenge(request, token):
    def find_key(token):
        if token == os.environ.get("ACME_TOKEN"):
            return os.environ.get("ACME_KEY")
        for k, v in os.environ.items():
            if v == token and k.startswith("ACME_TOKEN_"):
                n = k.replace("ACME_TOKEN_", "")
                return os.environ.get("ACME_KEY_{}".format(n))
    key = find_key(token)
    if key is None:
        raise Http404()
    return HttpResponse(key)
