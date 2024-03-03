from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer

"""
Post View
"""


@api_view(['GET', 'POST'])
def posts(request, post_id=None):
    """
    List all posts, or create a new post
    :param request:
    :param post_id:
    :return:
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):
    """
    Retrieve, update or delete a post
    :param request:
    :param post_id:
    :return:
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Like View
"""


@api_view(['POST'])
def like_post(request, post_id):
    """
    Like a post
    :param request:
    :param post_id:
    :return:
    """
    like_data = {'user': request.user.id, 'post': post_id}
    serializer = LikeSerializer(data=like_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def unlike_post(request, post_id):
    """
    Unlike a post
    :param request:
    :param post_id:
    :return:
    """
    post_like_instance = get_object_or_404(Like, user=request.user.id, post=post_id)
    post_like_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


"""
Comment View
"""


@api_view(['POST'])
def add_comment(request, post_id):
    """
    Add a comment
    :param request:
    :param post_id:
    :return:
    """
    comment_data = {'user': request.user.id, 'post': post_id, 'content': request.data.get('content')}
    serializer = CommentSerializer(data=comment_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_comment(request, post_id, comment_id):
    """
    Delete a comment
    :param request:
    :param post_id:
    :param comment_id:
    :return:
    """
    comment_instance = get_object_or_404(Comment, id=comment_id, post=post_id, user=request.user)
    comment_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
