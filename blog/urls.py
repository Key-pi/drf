from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>', views.post_detail, name='post-detail'),

    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),

    path('users/', views.UserListView.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),

    path('comment/reply/', views.reply_page, name="reply"),
    path('contact/', views.contact_form, name='contact'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
