# Generated by Django 4.0.6 on 2022-07-12 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
