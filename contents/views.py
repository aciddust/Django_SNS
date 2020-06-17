from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
#from django.db.models import Prefetch
from django.utils import timezone

from contents.models import Content, FollowRelation
from django.core.paginator import Paginator

from math import ceil

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        _per_page = 2
        context = super(HomeView, self).get_context_data(**kwargs)

        user = self.request.user
        followees = FollowRelation.objects.filter(follower=user).values_list('followee__id', flat=True)
        lookup_user_ids = [user.id] + list(followees)
        paginator = Paginator(Content.objects.select_related('user').prefetch_related('image_set').filter(
            user__id__in=lookup_user_ids), per_page=_per_page)

        max_len = len(Content.objects.select_related('user').prefetch_related('image_set').filter(user__id__in=lookup_user_ids))        
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['page_max'] = ceil(max_len / _per_page)
        return context

@method_decorator(login_required, name='dispatch')
class MyView(TemplateView):

    template_name = 'mypage.html'

    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)

        user = self.request.user
        
        lookup_user_ids = [user.id]
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set').filter(
            user__id__in=lookup_user_ids
        )
        paginator = Paginator(Content.objects.select_related('user').prefetch_related('image_set').filter(
        user__id__in=lookup_user_ids), per_page=10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        
        date = timezone.now() - user.created_date
        dday = int(date.days)
        if dday < 0:
            dday = 0

        if user.image == None:
            user.image.url = "/media/misc/basic.png"
        context['user_info'] = [user.name, user.email, str(dday), user.image, user.message]
        return context


@method_decorator(login_required, name='dispatch')
class RelationView(TemplateView):

    template_name = 'relation.html'

    def get_context_data(self, **kwargs):
        context = super(RelationView, self).get_context_data(**kwargs)

        user = self.request.user

        # 내가 팔로우하는 사람들
        try:
            followees = FollowRelation.objects.get(follower=user).followee.all()
            context['followees'] = followees
            context['followees_ids'] = list(followees.values_list('id', flat=True))
            context['followees_count'] = len(followees)
            
        except FollowRelation.DoesNotExist:
            context['followees_count'] = 0
        
        followers = FollowRelation.objects.select_related('follower').filter(followee__in=[user])
        context['followers'] = followers
        context['followers_count'] = len(followers)
        
        return context
