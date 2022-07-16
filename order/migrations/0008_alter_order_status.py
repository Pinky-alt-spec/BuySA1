# Generated by Django 4.0.6 on 2022-07-15 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_rename_adminnone_order_adminnote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preparing', 'Preparing'), ('OnShipping', 'OnShipping'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('On hold', 'On hold')], default='New', max_length=15),
        ),
    ]
