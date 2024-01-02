# from requests import Response
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.generics import RetrieveUpdateDestroyAPIView
#
#
# class PersonDetailAPIView(RetrieveUpdateDestroyAPIView):
#     # ...
#
#     @action(detail=True, methods=['post'])
#     def like(self, request, id=None):
#         post = self.get_object()
#         post.likes.add(request.user)
#         return Response({'message': 'Post liked successfully'}, status=status.HTTP_200_OK)
#
#     @action(detail=True, methods=['post'])
#     def unlike(self, request, id=None):
#         post = self.get_object()
#         post.likes.remove(request.user)
#         return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
#
#     @action(detail=True, methods=['post'])
#     def comment(self, request, id=None):
#         post = self.get_object()
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, post=post)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
