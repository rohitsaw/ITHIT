from .serializers import UserSerializer, StudentListSerializer, AssignmentListSerializer
from .models import Role, Student, Assignment


from django.contrib.auth import get_user_model # If used custom user model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView , ListAPIView, RetrieveUpdateDestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission
from rest_framework.filters import SearchFilter



# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},status=404)
        token, _ = Token.objects.get_or_create(user=user)
        obj = User.objects.get(username=username)
        data = {'token':token.key, 'id':obj.id, 'username':obj.username, 'first_name':obj.first_name, 'last_name':obj.last_name, 'email':obj.email }

        role = Role.objects.get(user=user)
        if role.isTeacher:
            data['isTeacher'] = True
        else:
            student = Student.objects.get(user=user)
            data['rollno'] = student.rollno
            data['year'] = student.year
        return Response( data, status=200)


# for logout
@api_view(["GET"])
def logout(request):
    request.user.auth_token.delete()
    data = {'msg': 'logout successfull'}
    return Response(data, status=200)


# for new user creation
class SignUp(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class teachersOnly(BasePermission):
    """
    Allows access only to "isTeacher" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role.isTeacher


class UserView(ListAPIView):
    permission_classes = (teachersOnly,)
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('year','rollno', )


class AssignmentView(generics.ListAPIView):
    serializer_class = AssignmentListSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter, )
    search_fields = ('header',)
    def get_queryset(self):
        if self.request.user.role.isTeacher:
            return Assignment.objects.all()
        year = self.request.user.student.year
        return Assignment.objects.filter(year = year)


@csrf_exempt
@api_view(["DELETE"])
@permission_classes((teachersOnly,))
def DeleteAssignment(request, pk):
    try:
        assignment = Assignment.objects.get(id=pk)
    except  Assignment.DoesNotExist:
        #print(assignment.teacher_id)
        #print(request.user.id)
        if assignment.teacher_id.id == request.user.id:
            assignment.delete()
            return Response({'msg: delete successfull'}, status=200)
        return Response({'error':'you do not have permissions'}, status=403)
    return Response({'error': 'assignment not found'}, status = 404)


@csrf_exempt
@api_view(["POST"])
@permission_classes((teachersOnly,))
def UploadDocs(request):
    #userid = request.data.get('userID',None)
    doc = request.FILES.get('file', None)
    header = request.data.get('header', None)
    year = request.data.get('year', None)
    if doc and header and year:
        if doc.size > 5000000:
            return Response({'error: file is too big'}, status=401)
        import magic
        filetype = magic.from_buffer(doc.read())
        print(filetype)
        from ITHIT.settings import check_allowed_file
        if not check_allowed_file(filetype):
            return Response({'error': 'file format is not allowed'}, status = 403)
        obj = Assignment.objects.create(docs=doc, header=header, year=year, teacher_id=request.user)
        obj.save()
            # teacher = Teacher.objects.get(user=userid)
            # teacher.assignments.add(obj)
        return Response({'msg: upload successfully'}, status=200)
    return Response({'error': 'something is missing'}, status=400)
