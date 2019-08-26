from tornado.web import url, StaticFileHandler

from .settings import settings
from ForumApp.apps.users.urls import urlpatterns as user_urls
from ForumApp.apps.community.urls import urlpatterns as com_urls


url_patterns = [
    url("/media/(.*)", StaticFileHandler, {
        'path': settings['MEDIA_ROOT']
    })
]


url_patterns += user_urls
url_patterns += com_urls
print(url_patterns)
