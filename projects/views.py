from django.core.paginator import Paginator
from django.shortcuts import render
from projects.models import Project, Image


def project_index(request):
    """ Display project index page which shows an overview
        of all projects with 6 projects shown per page.
    """
    project_list = Project.objects.all().order_by("-created_on")
    paginator = Paginator(project_list, 6)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    title = 'Projects'
    context = {
        'title': title,
        'projects': projects
    }
    return render(request, 'project_index.html', context)


def project_detail(request, pk):
    """ Display project detail page which shows a longer description
        of an individual project.
    """
    project = Project.objects.get(pk=pk)
    title = project.title
    context = {
        'title': title,
        'project': project
    }
    return render(request, 'project_detail.html', context)
