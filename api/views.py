from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action
from api.serializer import Regserializer, todoserializer
from api.models import Todo

# Create your views here.
class Todosview(ViewSet):
    authenthication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=todoserializer
    queryset=Todo.objects.all()

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    # def list(self,request,*args,**kw):
    #     qs=Todo.objects.all()
    #     serial=todoserializer(qs,many=True)
    #     return Response(data=serial.data)
    def create(self,request,*ar,**kw):
        seriali=todoserializer(data=request.data)
        if seriali.is_valid():
            print(request.user)
            Todo.objects.create(**seriali.validated_data,user=request.User)
            seriali.save()
            return Response(data=seriali.data)
        else:
            return Response(data=seriali.errors)
    def retrieve(self,request,*ar,**kw):
        id=kw.get("pk")
        qs=Todo.objects.get(id=id)
        serializer=todoserializer(qs,many=False)
        return Response(data=serializer.data)
    def destroy(self,request,*ar,**kw):
        id=kw.get("pk")
        qs=Todo.objects.get(id=id).delete()
        return Response(data="--->< Deleted ><---")
    
    def update(self,request,*ar,**kw):
        id=kw.get("pk")
        object=Todo.objects.get(id=id)
        serializer=todoserializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class todosmodelset(ModelViewSet):
    serializer_class=todoserializer
    queryset=Todo.objects.all()
    
    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*sr,**kw):
        qs=Todo.objects.filter(status=False)
        serializer=todoserializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*ar,**kw):
        qs=Todo.objects.filter(status=True)
        serializer=todoserializer(qs,many=True)
        return Response(data=serializer.data)
    