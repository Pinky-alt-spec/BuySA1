# Generated by Django 4.0.6 on 2022-07-12 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
