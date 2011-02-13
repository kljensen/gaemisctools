import pprint
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
try:
    import json
except:
    import simplejson as json

def make_simple_request_dict(r):
    """docstring for jsonify_noncallables"""
    def p_md(x):
        """docstring for p_md"""
        return x.items()
    def p_d(x):
        """docstring for p_d"""
        return dict(x)

    attrs = [
        ('body', None),
        ('method', None),
        ('scheme', None),
        ('script_name', None),
        ('path_info', None),
        ('content_type', None),
        ('remote_user', None),
        ('remote_addr', None),
        ('host', None),
        ('host_url', None),
        ('path_url', None),
        ('path', None),
        ('path_qs', None),
        ('headers', p_d),
        ('cookies', p_md),
        ('GET', p_md),
        ('POST', p_md),
    ]
    srd = {}
    for (a, c) in attrs:
        attr = getattr(r, a)
        if c:
            attr = c(attr)
        srd[a] = attr
    return srd
        
    

class AnalyzeRequest(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        srd = make_simple_request_dict(self.request)
        self.response.out.write('%s' % (json.dumps(srd, indent=4)))


BASEPATH = '/httpdebug'
application = webapp.WSGIApplication(
                                     [('%s/' % (BASEPATH), AnalyzeRequest)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()