from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('magazine/<slug:magazine>/', views.MagazineListView.as_view(), name='category_list'),
    path('profile/<str:username>/', views.UserPostListView.as_view(), name='profile_detail'),
    path('edit/profile/<int:pk>/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('edit/<int:pk>/', views.UpdatePostView.as_view(), name='edit_post'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('comment/<int:pk>/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/edit/<int:pk>/<int:id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/delete/<int:pk>/<int:id>/', views.CommentDeleteView.as_view(), name='delete_comment'),
]

