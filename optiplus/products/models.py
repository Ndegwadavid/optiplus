from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

class EyewearProduct(models.Model):
    FRAME_SHAPES = [
        ('round', 'Round'),
        ('square', 'Square'),
        ('oval', 'Oval'),
        ('rectangle', 'Rectangle'),
        ('cat_eye', 'Cat Eye'),
        ('aviator', 'Aviator'),
        ('wayfarer', 'Wayfarer'),
    ]
    
    FRAME_MATERIALS = [
        ('metal', 'Metal'),
        ('plastic', 'Plastic'),
        ('acetate', 'Acetate'),
        ('titanium', 'Titanium'),
        ('wood', 'Wood'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    frame_shape = models.CharField(max_length=20, choices=FRAME_SHAPES)
    frame_material = models.CharField(max_length=20, choices=FRAME_MATERIALS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='products/')
    image_2 = models.ImageField(upload_to='products/', blank=True)
    image_3 = models.ImageField(upload_to='products/', blank=True)
    
    # Specifications
    frame_width = models.CharField(max_length=50, blank=True)
    lens_width = models.CharField(max_length=50, blank=True)
    bridge_width = models.CharField(max_length=50, blank=True)
    temple_length = models.CharField(max_length=50, blank=True)
    
    # Stock and Status
    is_available = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    stock_qty = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    # SEO Fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_formatted_price(self):
        """Format price with KSH currency"""
        return f"KSH {self.price:,.2f}"

    def get_formatted_sale_price(self):
        """Format sale price with KSH currency"""
        if self.sale_price:
            return f"KSH {self.sale_price:,.2f}"
        return None

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    class Meta:
        ordering = ['-created_at']

    def get_discount_percentage(self):
        """Calculate the discount percentage"""
        if self.sale_price and self.price:
            discount = ((self.price - self.sale_price) / self.price) * 100
            return discount
        return 0