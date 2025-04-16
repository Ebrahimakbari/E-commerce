from django.urls import path, include
from . import views


bucket_url = [
    path("", view=views.BucketListView.as_view(), name="bucket"),
    path(
        "delete_obj_bucket/<path:key>",
        view=views.DeleteObjectBucketView.as_view(),
        name="delete_obj_bucket",
    ),
    path(
        "download_obj_bucket/<path:key>",
        view=views.DownloadObjectBucketView.as_view(),
        name="download_obj_bucket",
    ),
]

app_name = "home"
urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
    path("categories/<slug:category_slug>", view=views.HomeView.as_view(), name="categories"),
    path("bucket/", include(bucket_url)),
    path(
        "products/<slug:slug>/",
        view=views.ProductDetail.as_view(),
        name="product_detail",
    ),
]
