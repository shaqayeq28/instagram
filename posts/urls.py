from django.conf import settings
from django.urls import path
# from .views import InstaPostView, PostDetailView, LikeUnlikeView
from django.conf.urls.static import static

# from .views import InstaPostViewSet
# router.register("post-view", InstaPostViewSet, basename="post_view")


# urlpatterns =router.urls
urlpatterns = [
    # path('post/',InstaPostView.as_view(),name='post'),
    # path('post-detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    # path('like/<int:post_id>', LikeUnlikeView.as_view(), name='like')


     ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
