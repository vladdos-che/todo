from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import TodoList, Category


def redirect_view(request):
    return redirect('category/')


def todo(request):
    todos = TodoList.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        if "Add" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            todo = TodoList(title=title, content=content, due_date=date,
                            category=Category.objects.get(name=category))
            todo.save()
            return redirect("/todo")

        if "Delete" in request.POST:
            checked_list = request.POST.getlist('checkedbox')

            for i in range(len(checked_list)):
                todo = TodoList.objects.filter(id=int(checked_list[i]))
                todo.delete()

    return render(request, "todo.html",
                  {"todos": todos, "categories": categories})


def category(request):
    categories = Category.objects.all()

    if request.method == "POST":
        if "Add" in request.POST:
            name = request.POST["name"]
            category = Category(name=name)
            category.save()
            return redirect("/category")

        if "Delete" in request.POST:
            check = request.POST.getlist('check')

            for i in range(len(check)):
                try:
                    categ = Category.objects.filter(id=int(check[i]))
                    categ.delete()
                except BaseException:
                    return HttpResponse('<h1>Сначала удалите карточки с этими категориями!</h1>')

    return render(request, "category.html", {"categories": categories})
