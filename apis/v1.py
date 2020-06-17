from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
# from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from contents.models import Content, Image, FollowRelation, Comment
from accounts.models import User

from datetime import datetime

# add
from django.core.paginator import Paginator

search_buffer = []


@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):

    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status=status)


class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='패스워드를 입력해주세요.', status=400)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.response(message='입력 정보를 확인해주세요.', status=400)
        login(request, user)
        return self.response()


class UserLogoutView(BaseView):
    def get(self, request):
        logout(request)
        return self.response()


class UserCreateView(BaseView):
    def post(self, request):
        # Restful 하게 하기 위해선 POST, DELETE 다 나누어야 하지만, 편의상 POST만 사용하도록 하겠다.
        
        # 왜 request가 안들어오지?
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            return self.response(message='올바른 이메일을 입력해주세요.', status=400)

        username = request.POST.get('username', '')
        if not username:
            return self.response(message='이름을 입력해주세요.', status=400)
        
        password1 = request.POST.get('password1', '')
        if not password1:
            return self.response(message='패스워드를 입력해주세요.', status=400)
        
        password2 = request.POST.get('password2', '')
        if not password2:
            return self.response(message='패스워드 확인차 한번 더 입력해주세요.', status=400)

        if password1 and password2 and password1 != password2:
            return self.response(message='입력하신 패스워드가 서로 일치하지 않습니다.', status=400)

        try:
            user = User.objects.create_user(email, username, password1)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.', status=400)

        return self.response({'user.id': user.id})

@method_decorator(login_required, name='dispatch')
class LikeGetView(BaseView):
    def get(self, request):
        print(request)
        return self.response({})

@method_decorator(login_required, name='dispatch')
class LikeCreateView(BaseView):
    def post(self, request):
        post_id = request.POST.get('postid', '').strip()
        try:
            content = Content.objects.get(pk=int(post_id))

            if content.likes.filter(id=int(request.user.id)).exists():
                pass
            else:
                content.likes.add(request.user)

        except Exception as e:
            print(e)
            resp = {
                'messages' : '앗.. 잠시 후 다시 시도해주세요.',
                'count' : content.likes.count()
            }
            return self.response(resp)
        
        resp = {
            'messages' : '오홍홍 조와용 ^-^',
            'count' : content.likes.count()
        }

        return self.response(resp)

@method_decorator(login_required, name='dispatch')
class LikeDeleteView(BaseView):
    def post(self, request):
        post_id = request.POST.get('postid', '').strip()
        try:
            content = Content.objects.get(pk=int(post_id))

            if content.likes.filter(id=(request.user.id)).exists():
                content.likes.remove(request.user)
            else:
                pass

        except Exception as e:
            print(e)
            resp = {
                'messages' : '앗.. 잠시 후 다시 시도해주세요.',
                'count' : content.likes.count()
            }
            return self.response(resp)
        
        resp = {
            'messages' : '오홍홍 시러용 ^-^',
            'count' : content.likes.count()
        }

        return self.response(resp)


@method_decorator(login_required, name='dispatch')
class ContentCreateView(BaseView):
    def post(self, request):
        text = request.POST.get('text', '').strip()
        content = Content.objects.create(user=request.user, text=text)
        for idx, file in enumerate(request.FILES.values()):
            Image.objects.create(content=content, image=file, order=idx)
        return self.response({})


@method_decorator(login_required, name='dispatch')
class ContentDeleteView(BaseView):
    def post(self, request):
        try:
            post_id = int(request.POST.get('postId').strip())
            content = Content.objects.get(id=post_id)
            session_id = request.session.get('_auth_user_id')
            # if(content.user == User.objects.get(id=session_id)):
            if(content.user == User.objects.get(id=session_id)):
                content.delete()
            else:
                return self.response(message='잘못된 요청입니다.', status=400)
        except Exception as e:
            print(e)

        return redirect('/')

@method_decorator(login_required, name='dispatch')
class CommentGetView(BaseView):
    
    def get(self, request):
        try:
            post_id = request.GET.get('post','')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)
        
        try:
            comment = list()
            comment += Comment.objects.filter(content__id=int(post_id))
        except Comment.DoesNotExist:
            return self.response(message='댓글이 없습니다.', status=400)
        
        comment_list = list()
        for i in comment:
            comment_list.append({'uid': i.user.id,
                                 'image': i.user.image.url,
                                 'name':i.user.name,
                                 'comment':i.comment,
                                 'create':i.created_at})
        if len(comment_list) == 0:
            comment_list.append({'uid': 0,
                                 'image': '/media/misc/basic.png',
                                 'name': '댓글냥이',
                                 'comment': '아직 댓글이 없는 게시물이냥',
                                 'create':datetime.now()})
        
        return self.response(comment_list)


@method_decorator(login_required, name='dispatch')
class CommentPostView(BaseView):

    def post(self, request):
        try:
            user_id = request.user.id
            print('user_id : {}'.format(user_id))
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            post_id = request.POST.get('postid', '')
            comment = request.POST.get('comment', '')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)
        
        try:
            comment_instance = Comment(content=Content.objects.get(id=int(post_id)),
                                       user=User.objects.get(id=int(user_id)),
                                       comment=comment)
            comment_instance.save()
            return self.response(message='댓글을 달았습니다.', status=200)
        except Exception as e:
            print(e)
            return self.response(message='잘못된 요청일까요?.', status=400)


@method_decorator(login_required, name='dispatch')
class RelationCreateView(BaseView):

    def post(self, request):
        try:
            user_id = request.POST.get('id', '')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            relation = FollowRelation.objects.create(follower=request.user)

        try:
            if int(user_id) == int(request.user.id):
                # 자기 자신은 팔로우 안됨.
                raise IntegrityError
            else:
                relation.followee.add(user_id)
                relation.save()
        except IntegrityError:
            return self.response(message='자기 자신은 팔로우 할 수 없습니다.', status=400)

        return self.response({})


@method_decorator(login_required, name='dispatch')
class RelationDeleteView(BaseView):

    def post(self, request):
        try:
            user_id = request.POST.get('id', '')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            if int(user_id) == int(request.user.id):
                # 자기 자신은 언팔로우 안됨.
                raise IntegrityError
            else:
                relation.followee.remove(user_id)
                relation.save()
        except IntegrityError:
            return self.response(message='잘못된 요청입니다.', status=400)

        return self.response({})


class UserGetView(BaseView):
    def get(self, request):

        username = request.GET.get('username', '').strip()
        if username == '' or None or len(username) == 0:
            return self.response(message='사용자를 찾을 수 없습니다.', status=404)
        username_split = username.split(' ')
        try:
            user = list()
            user += User.objects.filter(name=username)
            user += User.objects.filter(name=username_split[0])
            user += User.objects.filter(name__startswith=username)
            user += User.objects.filter(name__endswith=username)
            if len(username_split) > 1:
                user += User.objects.filter(name=username_split[-1])
                user += User.objects.filter(name__endswith=username_split[-1])
            user = list(set(user))
        except User.DoesNotExist:
            self.response(message='사용자를 찾을 수 없습니다.', status=404)
        
        # Serialize
        userinfo = list()
        for i in user:
            try:
                if len(i.message) > 12:
                    i.message = i.message[:11]+'..'
                userinfo.append({'username':i.name, 'id':i.id, 'email':i.email.split('@')[0], 'image':i.image.url, 'message':i.message})
            except ValueError:
                userinfo.append({'username':i.name, 'id':i.id, 'email':i.email.split('@')[0], 'image':'/media/misc/basic.png', 'message': i.message})      
        
        return self.response(userinfo)

@method_decorator(login_required, name='dispatch')
class AccountImageUpdateView(BaseView):
    def post(self, request):
        for idx, file in enumerate(request.FILES.values()):
            user = User.objects.get(id=request.user.id) 
            user.image = file
            break # just 1 item.
        user.save()

        return self.response({})

@method_decorator(login_required, name='dispatch')
class AccountProfileUpdateView(BaseView):
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        user.message = request.POST.get('message', '').strip()[:255]
        user.save()
        return self.response({})