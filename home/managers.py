from django.db import models




class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)
    
    def q_search(self, q):
        return self.get_queryset().filter(models.Q(name__icontains=q) | models.Q(description__icontains=q))