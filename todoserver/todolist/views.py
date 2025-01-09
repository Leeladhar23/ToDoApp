from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TodoList, TodoItem
import json

@require_http_methods(["GET", "POST"])
def todo_list(request):
    if request.method == "GET":
        lists = TodoList.objects.all()
        return JsonResponse({"lists": [{"id": l.id, "name": l.name} for l in lists]})

    elif request.method == "POST":
        name = request.POST.get("name")
        if not name:
            return JsonResponse({"error": "Name is required"}, status=400)

        if TodoList.objects.filter(name=name).exists():
            return JsonResponse({"error": "List already exists"}, status=409)

        todo_list = TodoList.objects.create(name=name)
        return JsonResponse({"id": todo_list.id}, status=201)
    
    elif request.method == "DELETE":
        TodoList.objects.all().delete()
        return JsonResponse({}, status=204)
    
    
@require_http_methods(["GET", "DELETE"])
def todo_detail(request, pk):
    try:
        todo_list = TodoList.objects.get(pk=pk)
    except TodoList.DoesNotExist:
        return JsonResponse({"error": "List not found"}, status=404)

    if request.method == "GET":
        items = todo_list.todoitem_set.all()
        return JsonResponse({
            "id": todo_list.id,
            "name": todo_list.name,
            "items": [{"id": i.id, "title": i.title, "completed": i.completed, "deadline": i.deadline} for i in items]
        })

    elif request.method == "DELETE":
        todo_list.delete()
        return JsonResponse({}, status=204)
    
    
@require_http_methods(["POST", "GET", "DELETE"])
def todo_add(request, pk):
    try:
        todo_list = TodoList.objects.get(pk=pk)
    except TodoList.DoesNotExist:
        return JsonResponse({"error": "List not found"}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        completed = data.get("completed", False)
        deadline = data.get("deadline", None)

        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        item = TodoItem.objects.create(title=title, completed=completed, deadline=deadline, todo_list=todo_list)
        return JsonResponse({"id": item.id}, status=201)

    elif request.method == "GET":
        items = todo_list.todoitem_set.all()
        return JsonResponse({
            "items": [{"id": i.id, "title": i.title, "completed": i.completed, "deadline": i.deadline} for i in items]
        })
        
    elif request.method == "DELETE":
        todo_list.todoitem_set.all().delete()
        return JsonResponse({}, status=204)

@require_http_methods(["PATCH", "DELETE"])
def todo_update(request, pk, li):
    try:
        item = TodoItem.objects.get(pk=li, todo_list_id=pk)
    except TodoItem.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PATCH":
        data = json.loads(request.body)
        item.title = data.get("title", item.title)
        item.completed = data.get("completed", item.completed)
        item.deadline = data.get("deadline", item.deadline)
        item.save()
        return JsonResponse({"id": item.id})

    elif request.method == "DELETE":
        item.delete()
        return JsonResponse({}, status=204)
    