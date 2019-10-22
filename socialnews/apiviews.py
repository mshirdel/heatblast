from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


from .models import Story
from .serializers import StorySerializer, LoginSerializer


class StoryListCreateApiView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = StorySerializer

    def get(self, request):
        stories = Story.stories.all()
        serializer = self.serializer_class(stories,
                                           many=True,
                                           context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StorySerializer(data=request.data,
                                     partial=True,
                                     context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# class StoryDetail(APIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = StorySerializer
#     queryset = Story.stories.all()

#     def get_object(self, pk):
#         try:
#             return Story.stories.get(pk=pk)
#         except Story.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, pk):
#         serializer = self.serializer_class(self.get_object(pk))
#         return Response(serializer.data)

#     def put(self, request, pk):
#         story = self.get_object(pk)
#         serializer = self.serializer_class(story, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)


class StoryDetailApiView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    serializer_class = StorySerializer
    queryset = Story.stories


class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
