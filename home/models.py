from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from home.managers import ProductManager
# from ckeditor.fields import RichTextField




class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    is_child = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        #prevent a category to be itself parent
        if self.pk and self.parent and self.parent.pk == self.pk:
            self.parent = None
        self.slug = slugify(value=self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("home:categories", kwargs={"category_slug": self.slug})


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    # description = RichTextField()
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='products')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    default_objects = models.Manager()
    objects = ProductManager()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(value=self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("home:product_detail", kwargs={"slug": self.slug})
    