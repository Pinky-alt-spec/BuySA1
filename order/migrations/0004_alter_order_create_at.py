# Generated by Django 4.0.6 on 2022-07-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_rename_quality_orderproduct_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='create_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]