# Generated by Django 2.1.15 on 2020-05-11 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmanageapp', '0009_remove_order_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Book_NO',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
