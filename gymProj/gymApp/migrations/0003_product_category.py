# Generated by Django 5.0.2 on 2024-03-26 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymApp', '0002_attendance_category_membershipplan_trainer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gymApp.category'),
        ),
    ]