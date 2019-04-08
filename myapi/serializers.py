from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model
from django.contrib.auth.models import User
from .models import Student
from .models import Role, Assignment

#from .models import Student
UserModel = get_user_model()
from ITHIT.settings import students_key, teachers_key



class UserSerializer(serializers.Serializer):

    valid_field = ['username','first_name','last_name','email','password','year','rollno','isTeacher']

    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password= serializers.CharField()
    year = serializers.IntegerField()
    rollno = serializers.IntegerField()
    isTeacher = serializers.BooleanField(default=False)
    key = serializers.CharField(max_length = 200)
    def create(self, validated_data):
        #print(validated_data)
        if not validated_data['isTeacher'] and validated_data['key'] == students_key:
                user = self.create_user(validated_data)
                student = Student(user=user, year=validated_data['year'], rollno=validated_data['rollno'])
                student.save()
                role = Role(user=user, isTeacher=validated_data['isTeacher'])
                role.save()
                #return validated_data
        elif validated_data['isTeacher'] and validated_data['key'] == teachers_key:
                # teacher = Teacher(user=user)
                # teacher.save()
                user = self.create_user(validated_data)
                role = Role(user=user, isTeacher=validated_data['isTeacher'])
                role.save()
                validated_data['rollno'] = None
                validated_data['year'] = None
                #return validated_data
        else:
            raise serializers.ValidationError({'msg':'key is not valid'})

        validated_data['key'] = None
        return validated_data

    def create_user(self, validated_data):
            try:
                obj = UserModel.objects.get(username=validated_data['username'])
            except UserModel.DoesNotExist:
                user = UserModel.objects.create(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
                    )
                user.set_password(validated_data['password'])
                user.save()
                return user
            raise serializers.ValidationError({'msg' : 'username already exists'})


class StudentListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source = 'user.username')
    class Meta:
        model = Student
        fields = ('username', 'email', 'first_name', 'last_name', 'rollno', 'year')

class AssignmentListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher_id.first_name")
    class Meta:
        model = Assignment
        fields = ('id', 'docs', 'header', 'year', 'teacher_name')
