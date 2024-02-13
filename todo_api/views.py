from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializer import ToDoUserSerializer
from .models import ToDoUser

class UsersView(APIView):
        
        def get(self,request,*args,**kwargs):
            data = request.data
            user_email = data.get("email")
            if not user_email:
                users = ToDoUser.objects.all()
                serializer = ToDoUserSerializer(users,many=True)
            else:
                user = ToDoUser.objects.get(email=user_email)
                serializer = ToDoUserSerializer(user,many=False)
            return Response(serializer.data,status=HTTP_200_OK)
        
        def post(self,request,*args,**kwargs):
            data = request.data
            new_user_data = {
                 "first_name":data["first_name"],
                 "last_name":data["last_name"],
                 "email":data["email"],
            }
            serializer = ToDoUserSerializer(data=new_user_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            
class ToDoListView(APIView):
    def get(self,request,*args,**kwargs):
        data = request.data
        user_email = data.get("email")
        if not user_email:
            users = ToDoUser.objects.all()
            serializer = ToDoUserSerializer(users,many=True)
        else:
            user = ToDoUser.objects.get(email=user_email)
            serializer = ToDoUserSerializer(user,many=False)
        return Response(serializer.data,status=HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        ...
    
    def put(self,request,*args,**kwargs):
        ...
    
    def delete(self,request,*args,**kwargs):
        ...

class ToDoItemView(APIView):
    def get(self,request,*args,**kwargs):
        ...
    
    def post(self,request,*args,**kwargs):
        ...
    
    def put(self,request,*args,**kwargs):
        ...
    
    def delete(self,request,*args,**kwargs):
        ...