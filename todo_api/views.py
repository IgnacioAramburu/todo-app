from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from django.core.exceptions import ObjectDoesNotExist
from .serializer import ToDoListSerializer, ToDoItemSerializer
from .models import  ToDoList, ToDoItem

class ToDoListView(APIView):

    def get(self,request,*args,**kwargs):
        filter_data = request.data
        target_list_id = kwargs.get('id')

        #Check if query_params include_items is present and its value. If true returns ToDoList instances with related ToDoItem instances info. If false, only ToDoList
        include_items = request.query_params.get('include_items', None)
        include_items = include_items if include_items is not None else "false"
        include_items = True if include_items.lower() == "true" else False

        serializer_context = {'include_items': include_items}

        try:
            if not target_list_id and not filter_data:
                lists = ToDoList.objects.all()
                serializer = ToDoListSerializer(lists,many=True,context=serializer_context)
                return Response(serializer.data, status = HTTP_200_OK)
            
            if target_list_id:
                list = ToDoList.objects.get(id=target_list_id)
                serializer = ToDoListSerializer(list,many=False,context=serializer_context)
                return Response(serializer.data, status = HTTP_200_OK)

            lists = ToDoList.objects.filter(**filter_data)
            serializer = ToDoListSerializer(lists,many=True,context=serializer_context)
            return Response(serializer.data, status = HTTP_200_OK)
        except ObjectDoesNotExist:
                return Response({'detail': 'Results not found matching given criteria'}, status = HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Internal Server Error'}, status = HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self,request,*args,**kwargs):
        new_list_data = request.data

        serializer = ToDoListSerializer(data=new_list_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = HTTP_201_CREATED)
        
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
    def put(self,request,*args,**kwargs):
        data_to_update = request.data
        target_list_id = kwargs.get('id')
        
        try:
            _list = ToDoList.objects.get(id=target_list_id)
            serializer = ToDoListSerializer(_list,data_to_update,partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = HTTP_202_ACCEPTED)
            
            return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'detail': 'No list found to update data'}, status = HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Internal Server Error'}, status = HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self,request,*args,**kwargs):
        target_list_id = kwargs.get('id')

        try:
            _list = ToDoList.objects.get(id=target_list_id)

            _list.delete()

            return Response({'detail': 'Sucessfully deleted'}, status = HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'detail': 'No list found'}, status = HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Internal Server Error'}, status = HTTP_500_INTERNAL_SERVER_ERROR)

class ToDoItemView(APIView):

    def get(self,request,*args,**kwargs):
        filter_data = request.data
        target_item_id = kwargs.get('id')
        target_list_id = kwargs.get('list_id')

        try:
            if not target_item_id and not target_list_id and not filter_data:
                lists = ToDoItem.objects.all()
                serializer = ToDoItemSerializer(lists,many=True)
                return Response(serializer.data, status = HTTP_200_OK)
            
            if target_item_id:
                item = ToDoItem.objects.get(id=target_item_id)
                serializer = ToDoItemSerializer(item,many=False)
                return Response(serializer.data, status = HTTP_200_OK)
            
            if target_list_id:
                _list = ToDoList.objects.get(id=target_list_id)
                filter_data["list"] = _list

            items=ToDoItem.objects.filter(**filter_data)
            serializer = ToDoItemSerializer(items,many=True)
            return Response(serializer.data, status = HTTP_200_OK)
        except ObjectDoesNotExist:
                return Response({'detail': 'Results not found matching given criteria'}, status = HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Internal Server Error'}, status = HTTP_500_INTERNAL_SERVER_ERROR)

        
    def post(self,request,*args,**kwargs):
        new_item_data = request.data
        list_id = kwargs.get('list_id')

        try:
            _list = ToDoList.objects.get(id=list_id)

            new_item_data["list"] = _list.id

        except ObjectDoesNotExist:
            return Response({'detail':"List not found. Operation cannot be performed"}, status = HTTP_409_CONFLICT)
        else:
            item_serializer = ToDoItemSerializer(data=new_item_data)

            if item_serializer.is_valid():
                item_serializer.save()
                list_data_update = {"completed":False,"size":_list.size+1}
                list_serializer = ToDoListSerializer(_list,list_data_update,partial=True)

                if list_serializer.is_valid():
                    list_serializer.save()

                return Response(item_serializer.data, status = HTTP_201_CREATED)
            
            return Response(item_serializer.errors, status = HTTP_400_BAD_REQUEST)
    
    def put(self,request,*args,**kwargs):
        data_to_update = request.data
        target_item_id = kwargs.get('id')

        try:
            item = ToDoItem.objects.get(id=target_item_id)

            item_serializer = ToDoItemSerializer(item,data_to_update,partial=True)

            if item_serializer.is_valid():
                item_serializer.save()

                #If any uncompleted item remains in the list, including the recently updated, 'completed' in ToDoList should be false, else true
                uncompleted_items = ToDoItem.objects.filter(list=item.list.id,completed=False)
                list_data_update = {"completed":False} if uncompleted_items else {"completed":True}
                list_serializer = ToDoListSerializer(item.list,list_data_update,partial=True)

                if list_serializer.is_valid():
                    list_serializer.save()

                return Response(item_serializer.data, status = HTTP_202_ACCEPTED)
            
            return Response(item_serializer.errors, status = HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'detail': 'No item found to update data'}, status = HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Internal Server Error'}, status = HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self,request,*args,**kwargs):
        target_item_id = kwargs.get('id')

        try:
            item = ToDoItem.objects.get(id=target_item_id)
            
            item.delete()

            #If any uncompleted item remains in the list, including the recently updated, 'completed' in ToDoList should be false, else true
            uncompleted_items = ToDoItem.objects.filter(list=item.list.id,completed=False)
            list_data_update = {"completed":False} if uncompleted_items else {"completed":True}
            list_data_update = {**list_data_update,'size':item.list.size-1}
            list_serializer = ToDoListSerializer(item.list,list_data_update,partial=True)

            if list_serializer.is_valid():
                list_serializer.save()

            return Response({'detail': 'Sucessfully deleted'}, status = HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'detail': 'No results found'}, status = HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Internal Server Error'}, status = HTTP_500_INTERNAL_SERVER_ERROR)