from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden,HttpResponseRedirect
from django.contrib.auth.views import login
from token import token_generator
from django.core.urlresolvers import reverse
from forms import *

def registration(request):
    register_form = RegistrationForm()
    phones_formset = AdditionalPhonesFormset()
    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            registered_user = register_form.save()
            phones_formset = AdditionalPhonesFormset(request.POST, 
                                request.FILES, instance = registered_user)
            if phones_formset.is_valid():
                phones_formset.save()
                return HttpResponseRedirect(reverse("registration_success"))
    return render(request,"register.html",{"register_form":register_form,
                                        "phones_formset":phones_formset})

def login(request):
    return login(request, template_name='login_form.html',
          authentication_form=MultiphoneAuthForm,
          extra_context=None)

def request_result(request, result):
    return HttpResponse(result)

def approve_phone(request, phone_id):
    add_phone_obj = get_object_or_404(AdditionalPhone, 
                                         pk = phone_id)
    if token_generator.check_token(add_phone_obj.user, add_phone_obj.phone, 
                                        request.GET.get('hash',"")):
        try:
            add_phone_obj.set_active()
        except PhoneIsAlreadyApproved:
            return HttpResponseRedirect(reverse("approve_fail"))
    return HttpResponseRedirect(reverse("approve_success"))
