import os
import uuid
import json

import aiofiles
from playhouse.shortcuts import model_to_dict

from ForumApp.main_app.handler import RedisHandler
from ForumApp.apps.utils.decorators import authenticated_async
from ForumApp.apps.utils.funcs import json_serialize
from .models import *
from .forms import *


class GroupHandler(RedisHandler):

    async def get(self):
        # 获取小组列表
        json_response = []
        community_query = CommunityGroup.extend()

        # 根据类别进行过滤
        category = self.get_argument("category", None)
        if category:
            community_query = community_query.filter(CommunityGroup.category==category)

        # 根据参数进行排序
        orders = self.get_argument("orders", None)
        if orders == "new":
            community_query = community_query.order_by(CommunityGroup.add_time.desc())
        elif orders == "hot":
            community_query = community_query.order_by(CommunityGroup.member_nums.desc())

        # 限制
        limit = self.get_argument("limit")
        if limit:
            community_query = community_query.limit(int(limit))

        groups = await self.application.objects.execute(community_query)
        for group in groups:
            group_dict = model_to_dict(group)
            # 由于图片保存的是media相对路径,所以要把路径补全以后再返回
            group_dict["front_image"] = f"{self.settings['site_url']}/media/{group_dict['front_image']}/"
            json_response.append(group_dict)
            # json.dumps -> 当default被指定时,其应该是一个函数,每当某个对象无法被序列化时它会被调用
        await self.finish(json.dumps(json_response, default=json_serialize))

    # 验证用户是否登录
    @authenticated_async
    async def get(self):
        json_response = {}
        # 不能使用jsonForm,因为要上传封面图片
        form = CommunityForm(self.request.body_arguments)
        if form.validate():
            # 完成图片字段的验证
            files_meta = self.request.files.get("front_image", None)
            if not files_meta:
                self.set_status(400)
                json_response["front_image"] = "请上传图片"
            else:
                # 完成图片保存,并将值保存至数据库
                # 防止文件名重复,要动态生成文件名
                filename = None
                for meta in files_meta:
                    filename = meta["filename"]
                    filename = f"{uuid.uuid1()}_{filename}"
                    filepath = os.path.join(self.settings["MEDIA_ROOT"], filename)
                    async with aiofiles.open(filepath, 'wb') as f:
                        await f.write(meta["body"])
                group = await self.application.objects.create(
                    CommunityGroup, creator=self.current_user, name=form.name.data, categroy=form.category.data,
                    desc=form.desc.data, notice=form.notice.data, front_image=filename
                )
                json_response["id"] = group.id
        else:
            self.set_status(400)
            for field in form.errors:
                json_response[field] = form.errors[field][0]
        await self.finish(json_response)


class GroupMemberHandler(RedisHandler):

    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        json_response = {}
        params = self.request.body.decode("utf8")
        params = json.loads(params)
        form = GroupApplyForm.from_json(params)
        if form.validate():
            group = None
            try:
                group = await self.application.objects.get(CommunityGroup, id=int(group_id))
                existed = await self.application.objects.get(
                    CommunityGroupMember, community=group, user=self.current_user
                )
                if existed:
                    self.set_status(400)
                    json_response["non_fields"] = "不能重复加入同一小组"
            except CommunityGroup.DoesNotExist as e:
                self.set_status(404)
            except CommunityGroupMember.DoesNotExist as e:
                community_memeber = await self.application.objects.create(
                    CommunityGroupMember, user=self.current_user, community=group, reason=form.apply_reason.data
                )
                json_response["id"] = community_memeber.id
            else:
                self.set_status(400)
                for field in form.errors:
                    json_response[field] = form.errors[field][0]
            await self.finish(json_response)


class GroupDetailHandler(RedisHandler):
    @authenticated_async
    async def get(self, group_id):
        # 获取小组的基本信息
        json_response = {}
        try:
            group_data = {}
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            group_data["name"] = group.data
            group_data["desc"] = group.desc
            group_data["notice"] = group.notice
            group_data["member_nums"] = group.member_nums
            group_data["front_image"] = f"{self.settings['site_url']}/media/{group_data['front_image']}/"
            json_response = group_data
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)
        await self.finish(json_response)


class PostHandler(RedisHandler):
    @authenticated_async
    async def get(self, group_id):
        # 获取小组内的帖子
        post_list = []
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            group_member = await self.application.objects.get(
                CommunityGroupMember, user=self.current_user, community=group, status="agree"
            )
            post_query = Post.extend()
            c = self.get_argument("c", None)
            if c == "hot":
                post_query = post_query.filter(Post, is_hot=True)
            if c == "excellent":
                post_query = post_query.filter(Post, is_execellent=True)
            posts = await self.application.objects.execute(post_query)

            for post in posts:
                item_dict = {
                    "user": {
                        "id": post.user.id,
                        "nick_name": post.user.nick_name
                    },
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "comment_nums": post.comment_nums
                }
                post_list.append(item_dict)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)

        await self.finish(json.dumps(post_list))

    @authenticated_async
    async def post(self, group_id):
        # 小组内发帖
        json_response = {}
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            group_member = await self.application.objects.get(
                CommunityGroupMember, user=self.current_user, community=group, status="agree"
            )
            params = self.request.body.decode("utf8")
            params = json.loads(params)
            form = PostForm.from_json(params)
            if form.validate():
                post = await self.application.objects.create(
                    Post, user=self.current_user, title=form.title.data, content=form.content.data, group=group
                )
                json_response["id"] = post.id
            else:
                self.set_status(400)
                for field in form.errors:
                    json_response[field] = form.errors[field][0]
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)
        await self.finish(json_response)


class PostDetailHandler(RedisHandler):

    @authenticated_async
    async def get(self, post_id):
        # 获取帖子的详情
        flg = 0
        json_response = {}
        post_detail = await self.application.objects.execute(Post.extend().where(id==int(post_id)))
        for data in post_detail:
            json_response["user"] = model_to_dict(data.user)
            json_response["title"] = data.title
            json_response["content"] = data.content
            json_response["comment_nums"] = data.comment_nums
            json_response["add_time"] = data.add_time.strftime("%Y-%m-%d")
            flg += 1
        if not flg:
            self.set_status(404)
        await self.finish(json_response)


class PostCommentHandler(RedisHandler):
    @authenticated_async
    async def get(self, post_id):
        json_response = []
        try:
            post_comments = await self.application.objects.execute(
                PostComment.extend().where(PostComment.post_id==int(post_id), PostComment.parent_comment.is_null(True)).order_by(PostComment.add_time.desc)
            )

            for item in post_comments:
                is_like = False
                try:
                    comment_like = await self.application.objects.get(
                        CommentLike, post_comment_id=item.id, user_id=self.current_user
                    )
                    is_like = True
                    item_dict = {
                        "user": model_to_dict(item.user),
                        "content": item.content,
                        "reply_nums": item.reply_nums,
                        "like_nums": item.like_nums,
                        "is_like": is_like,
                        "id": item.id
                    }

                    json_response.append(item_dict)
                except CommentLike.DoesNotExist:
                    pass
        except Post.DoesNotExist as e:
            self.set_status(404)
        await self.finish(json.dumps(json_response))

    @authenticated_async
    async def post(self, post_id):
        # 新增评论
        json_response = {}
        params = self.request.body.decode("utf8")
        params = json.loads(params)
        form = PostCommentForm.from_json(params)
        if form.validate():
            try:
                post = await self.application.objects.get(Post, id=int(post_id))
                post_comment = await self.application.objects.create(
                    PostComment, user=self.current_user, post=post, content=form.content.data
                )
                json_response["id"] = post_comment.id
                json_response["user"] = {"id": self.current_user.id, "nick_name": self.current_user.nick_name}
            except Post.DoesNotExist as e:
                self.set_status(404)
        else:
            self.set_status(400)
            for field in form.errors:
                json_response[field] = form.errors[field][0]
        await self.finish(json_response)
