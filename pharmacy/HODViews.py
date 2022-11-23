from django.shortcuts import render
from django.contrib import messages
from .decorators import *

from .forms import *
from .models import *


def adminDashboard(request):
    out_of_stock = Stock.objects.filter(quantity__lte=0).count()
    total_stock = Stock.objects.all().count()

    expired = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()),
                                  output_field=BooleanField())
    ).filter(expired=True).count()

    context = {
        "expired_total": expired,
        "out_of_stock": out_of_stock,
        "total_drugs": total_stock,
    }
    return render(request, 'hod_templates/admin_dashboard.html', context)


def addStock(request):
    form = StockForm(request.POST, request.FILES)
    if form.is_valid():
        form = StockForm(request.POST, request.FILES)

        form.save()
        return redirect('add_stock')

    context = {
        "form": form,
        "title": "Añadir medicina"
    }
    return render(request, 'hod_templates/add_stock.html', context)


def manageStock(request):
    stocks = Stock.objects.all().order_by("-id")
    ex = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()),
                                  output_field=BooleanField())
    ).filter(expired=True)
    eo = Stock.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()),
                                  output_field=BooleanField())
    ).filter(expired=False)

    context = {
        "stocks": stocks,
        "expired": ex,
        "expa": eo,
        "title": "Manage Stocked Drugs"
    }

    return render(request, 'hod_templates/manage_stock.html', context)


def addCategory(request):
    try:
        form = CategoryForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Category added Successfully!")

                return redirect('add_category')
    except:
        messages.error(request, "Category Not added! Try again")

        return redirect('add_category')

    context = {
        "form": form,
        "title": "Add a New Drug Category"
    }
    return render(request, 'hod_templates/add_category.html', context)


def hodProfile(request):
    customuser = CustomUser.objects.get(id=request.user.id)
    staff = AdminHOD.objects.get(admin=customuser.id)

    form = HodForm()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.save()

        staff = AdminHOD.objects.get(admin=customuser.id)
        form = HodForm(request.POST, request.FILES, instance=staff)
        staff.address = address

        staff.mobile = mobile
        staff.save()

        if form.is_valid():
            form.save()

    context = {
        "form": form,
        "staff": staff,
        "user": customuser
    }

    return render(request, 'hod_templates/hod_profile.html', context)


def editAdmin(request):
    customuser = CustomUser.objects.get(id=request.user.id)
    staff = AdminHOD.objects.get(admin=customuser.id)

    form = HodForm()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.save()

        staff = AdminHOD.objects.get(admin=customuser.id)
        form = HodForm(request.POST, request.FILES, instance=staff)
        staff.address = address

        staff.mobile = mobile
        staff.save()

        if form.is_valid():
            form.save()

    context = {
        "form": form,
        "staff": staff,
        "user": customuser
    }

    return render(request, 'hod_templates/edit-profile.html', context)


def editStock(request, pk):
    drugs = Stock.objects.get(id=pk)
    form = StockForm(request.POST or None, instance=drugs)

    if request.method == "POST":
        if form.is_valid():
            form = StockForm(request.POST or None, instance=drugs)

            category = request.POST.get('category')
            drug_name = request.POST.get('drug_name')
            quantity = request.POST.get('quantity')
            # email=request.POST.get('email')

            try:
                drugs = Stock.objects.get(id=pk)
                drugs.drug_name = drug_name
                drugs.quantity = quantity
                drugs.save()
                form.save()
                messages.success(request, 'Receptionist Updated Succefully')
            except:
                messages.error(request,
                               'An Error Was Encounterd Receptionist Not Updated')

    context = {
        "drugs": drugs,
        "form": form,
        "title": "Edit Stock"

    }
    return render(request, 'hod_templates/edit_drug.html', context)


def deleteDrug(request, pk):
    try:

        drugs = Stock.objects.get(id=pk)
        if request.method == 'POST':
            drugs.delete()
            messages.success(request, "Pharmacist  deleted successfully")

            return redirect('manage_stock')

    except:
        messages.error(request, "Pharmacist aready deleted")
        return redirect('manage_stock')

    return render(request, 'hod_templates/sure_delete.html')


def receiveDrug(request, pk):
    receive = Stock.objects.get(id=pk)
    form = ReceiveStockForm()
    try:
        form = ReceiveStockForm(request.POST or None)

        if form.is_valid():
            form = ReceiveStockForm(request.POST or None, instance=receive)

            instance = form.save(commit=False)
            instance.quantity += instance.receive_quantity
            instance.save()
            form = ReceiveStockForm()

            messages.success(request,
                             str(instance.receive_quantity) + " " + instance.drug_name + " " + "drugs added successfully")

            return redirect('manage_stock')


    except:
        messages.error(request, "An Error occured, Drug quantity Not added")

        return redirect('manage_stock')
    context = {
        "form": form,
        "title": "Add Drug"

    }
    return render(request, 'hod_templates/modal_form.html', context)


def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(
            instance.drug_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("manage_stock")
    context = {
        "instance": queryset,
        "form": form,
        "title": "Reorder Level"
    }

    return render(request, 'hod_templates/reorder_level.html', context)


def drugDetails(request, pk):
    stocks = Stock.objects.get(id=pk)
    # prescrip=stocks.prescription_set.all()
    # stocks=stocks.dispense_set.all()

    context = {
        "stocks": stocks,
        # "prescription":prescrip,
        # "stocks":stocks

    }
    return render(request, 'hod_templates/view_drug.html', context)
