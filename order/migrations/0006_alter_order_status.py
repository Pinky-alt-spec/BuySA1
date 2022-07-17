# Generated by Django 4.0.6 on 2022-07-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_create_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Being Prepared', 'Being Prepared'), ('Shipped', 'Shipped'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=15),
        ),
    ]