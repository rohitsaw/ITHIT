from django.urls import path
from myapi.views import *

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('signup/', SignUp.as_view()),
    #path('users/<int:year>/', UserByYear.as_view()),
    path('upload/', UploadDocs),
    #path('assignment/<int:year>', AssignmentByYear.as_view()),

    path('users/', UserView.as_view()),
    path('assignment/<int:pk>', DeleteAssignment),
    path('assignment/', AssignmentView.as_view()),
    #path('assignment/<int:pk>', DeleteAssignment),
    #path('users/', UserList.as_view()),
    #path('sample/', UserAPIView.as_view())
]
