from django.shortcuts import get_object_or_404
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PostAPIv2List(APIView):
    def get(self, request):
        posts = Post.objects.get_published()
        serializer = PostSerializer(
            instance=posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PostAPIv2Detail(APIView):
    def get_post(self, pk):
        post = get_object_or_404(
            Post.objects.get_published(),
            pk=pk
        )
        return post

    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(
            instance=post,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(
            instance=post,
            data=request.data,
            partial=True,
            many=False,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )

    def delete(self, request, pk):
        post = self.get_post(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
