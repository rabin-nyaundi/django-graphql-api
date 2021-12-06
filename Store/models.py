from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=10, unique=True,  blank=True, null=True)
    category = models.ForeignKey('Category', related_name="product", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=None) 
    image = models.ImageField(null=True, blank=True, default="https://bit.ly/30cn4o9")
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['date_created']


    def __str__(self):
        return self.name