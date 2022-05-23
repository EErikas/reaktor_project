from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.conf import settings
from .parser import PackageParser


# Helper functions
def show_warnings(request, warnings):
    for warning in warnings:
        if warning.get('level') == 'critical':
            messages.warning(request, warning.get('description', 'Unknown critical error'))
        elif warning.get('level') == 'warning':
            messages.info(request, warning.get('description', 'Unknown warning'))
        else:
            messages.success(request, warning.get('description', 'Unknown message'))


def is_debug(user):
    return settings.DEBUG


# Application views (Always available)
def file_upload(request):
    if request.method == 'POST':

        # If file is successfully read, it's converted to string
        # otherwise, an empty string is passed
        if request.FILES.get('file'):
            file_text = request.FILES.get('file').read().decode('utf-8')
        else:
            file_text = ''

        data = PackageParser(file_text)
        show_warnings(request, data.get_warnings())
        if data.no_critical():
            request.session['packages'] = data.get_packages()
            request.session['installed'] = data.get_installed()
            request.session['reverse_dependencies'] = data.get_reverse_dependencies()
            return redirect('package-list')
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
        return redirect('package-list')
    print(request.session.get('reverse_dependencies', {}).get(package_name))
    return render(request, 'package_page.html', context={
        'title': f'Details of {matching_pkgs[0].get("name")}',
        'package': matching_pkgs[0],
        'reverse_dependencies': request.session.get('reverse_dependencies', {}).get(package_name)
    })


# Debug views (only available in debug mode)
'''
user_passes_test is built in function that is used by django to check if user hsa permission to access the view
In this application there's no user management implemented, nevertheless this decorator is used as an easy way to 
redirect from the debug url in production mode. Therefore in this case, the 'login_url' is used for simply redirecting 
to a working url
'''


@user_passes_test(is_debug, login_url='package-list')
def dump_packages(request):
    return JsonResponse(request.session.get('packages', []), safe=False)


@user_passes_test(is_debug, login_url='package-list')
def dump_installed_packages(request):
    return JsonResponse(request.session.get('installed', []), safe=False)


@user_passes_test(is_debug, login_url='package-list')
def dump_reverse_dependencies(request):
    return JsonResponse(request.session.get('reverse_dependencies', {}))


@user_passes_test(is_debug, login_url='package-list')
def clear_session(request):
    request.session.clear()
    messages.success(request, 'Session cleared successfully')
    return redirect('package-list')
