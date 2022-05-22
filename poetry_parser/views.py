from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from .parser import PackageParser


def show_warnings(request, warnings):
    for warning in warnings:
        if warning.get('level') == 'critical':
            messages.warning(request, warning.get('description', 'Unknown critical error'))
        elif warning.get('level') == 'warning':
            messages.info(request, warning.get('description', 'Unknown warning'))
        else:
            messages.success(request, warning.get('description', 'Unknown message'))


# def get_session_package_list(request):
#     request.session.get('packages',[])
# Create your views here.
def index(request):
    # if len(packages) == 0:
    #     return redirect('upload')
    return redirect('package-list')


def file_upload(request):
    if request.method == 'POST':
        file = request.FILES['file'].read()
        opa = PackageParser(file.decode('utf-8'))
        show_warnings(request, opa.get_warnings())
        if opa.no_critical():
            request.session['packages'] = opa.get_packages()
            request.session['installed'] = opa.get_installed()
            request.session['reverse_dependencies'] = opa.get_reverse_dependencies()
            # return JsonResponse(opa.get_packages(), safe=False)
            return redirect('package-list')
            # return render(request, 'packages.html', context={
            #     'title': 'List of packages',
            #     'packages': opa.get_packages()
            # })
            # return JsonResponse(opa.get_packages(), safe=False)

        # print(opa.get_packages())
        # return JsonResponse(opa.get_packages(), safe=False)
    # else:
    return render(request, 'upload.html')


def package_list(request):
    packages = request.session.get('packages', [])
    if len(packages) == 0:
        messages.warning(request, 'No packages found, upload poetry.lock file first')
        return redirect('upload')
    return render(request, 'packages.html', context={
        'title': 'List of packages',
        'packages': packages
    })


def package_page(request, package_name):
    packages = request.session.get('packages', [])
    # Find packages with matching name
    matching_pkgs = [package for package in packages
                     if package.get('name') == package_name]
    if len(matching_pkgs) == 0:
        messages.warning(request, f'Package "{package_name}" is not installed')
        return redirect('upload')
    print(request.session.get('reverse_dependencies', {}).get(package_name))
    return render(request, 'package_page.html', context={
        'title': f'Details of {matching_pkgs[0].get("name")}',
        'package': matching_pkgs[0],
        'reverse_dependencies': request.session.get('reverse_dependencies', {}).get(package_name)
    })
