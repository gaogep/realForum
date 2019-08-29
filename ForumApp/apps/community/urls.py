from tornado.web import url

from .handler import GroupHandler, GroupMemberHandler, GroupDetailHandler, \
                     PostHandler, PostDetailHandler, PostCommentHandler

urlpatterns = [
    url('/groups/?', GroupHandler),
    url('/groups/([0-9]+)/?', GroupDetailHandler),
    url('/groups/([0-9]+)/members/?', GroupMemberHandler),
    url('/gorups/([0-9]+)/post/?', PostHandler),
    url('/posts/([0-9]+)/?', PostDetailHandler),
    url('/posts/([0-9]+)/comments?', PostCommentHandler),
]
