from django.urls import path
from . import views
from .views import ArticleCommentListCreateView


urlpatterns = [
    path('list/', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_id>/comments/', ArticleCommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/delete/<int:comment_pk>/', views.delete_comment, name='delete_comment'),

]
