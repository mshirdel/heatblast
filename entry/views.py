from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import EntrySerializer
from .models import Entry


class EntryListCreateView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serialzier_class = EntrySerializer

    def get(self, request):
        serializer = EntrySerializer(Entry.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serialzier = self.serialzier_class(data=request.data,
                                           partial=True)
        if serialzier.is_valid():
            serialzier.save(owner=request.user)
            return Response(serialzier.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serialzier.errors,
                            status=status.HTTP_400_BAD_REQUEST)
