import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from .models import Product, Category
from django.contrib import messages
from . import tasks
from . import forms
from utils import IsAdminUserMixin



class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if category_slug:
            category = categories.filter(slug=category_slug).first()
            products = products.filter(category=category)
        categories = categories.filter(is_child=False)
        return render(
            request, template_name="home/home.html", context={"products": products, 'categories':categories}
        )


class ProductDetail(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs.get("slug"))
        if product.exists():
            return render(request, "home/detail.html", {"product": product.first()})
        messages.error(request, message="product not found")
        return redirect("home:home")


class BucketListView(IsAdminUserMixin, View):
    form_class = forms.UploadFileForm

    def get(self, request):
        form = self.form_class()
        objects = tasks.get_bucket_list()
        return render(request, "home/bucket.html", {"objects": objects, "form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["upl_file"]
            # Save the file to a temporary location
            temp_file_path = os.path.join(settings.AWS_LOCAL_DIRECTORY, file.name)
            with open(temp_file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Upload the file to S3
            result = tasks.upload_obj_bucket.delay(
                temp_file_path, object_name=file.name
            )
            result.wait()  # TODO: we can add loading or uploading page with ajax and make it async
            # Remove the temporary file
            os.remove(temp_file_path)
            messages.success(request, "uploaded!")
            return redirect("home:bucket")
        messages.error(request, "invalid files")
        return redirect("home:bucket")


class DeleteObjectBucketView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_obj_bucket.delay(key)
        messages.success(request, "object will delete soon...")
        return redirect("home:bucket")


class DownloadObjectBucketView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_obj_bucket.delay(key)
        messages.success(request, "object will download soon...")
        return redirect("home:bucket")
