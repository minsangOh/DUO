from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics

import logging

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE'])
def article_detail(request, article_pk):
    try:
        article = Article.objects.get(pk=article_pk)
    except Article.DoesNotExist:
        # 게시글이 존재하지 않을 때 빈 객체 반환
        return Response({})

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # article_id에 따라 댓글을 반환
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article_id=article_id)

    def perform_create(self, serializer):
        article_id = self.kwargs['article_id']
        serializer.save(author=self.request.user, article_id=article_id)

    # 디버깅용 코드. 요청 데이터를 로그로 남겨, 서버가 어떤 데이터를 받고 있는지 확인
    # def create(self, request, *args, **kwargs):
    #     logger.info(f"Received data: {request.data}")
    #     return super().create(request, *args, **kwargs)


@api_view(['DELETE'])
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    # 요청 사용자가 댓글 작성자이거나 삭제 권한이 있는지 확인
    if request.user == comment.author or request.user.is_staff:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        # 사용자가 삭제 권한이 없으면 HTTP 403 Forbidden 응답 반환
        return Response(status=status.HTTP_403_FORBIDDEN)
