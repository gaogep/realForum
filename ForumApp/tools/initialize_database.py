from peewee import MySQLDatabase

from ForumApp.main_app.settings import settings
from ForumApp.apps.users.models import User
from ForumApp.apps.community.models import CommunityGroup, CommunityGroupMember

database = MySQLDatabase(**settings["db"])
database.create_tables([User])
database.create_tables([CommunityGroup, CommunityGroupMember])