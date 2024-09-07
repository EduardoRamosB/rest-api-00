# Generated by Django 5.1.1 on 2024-09-06 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelter', '0003_alter_adoption_volunteer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('available', 'Available'), ('requested', 'Requested'), ('pending', 'Pending'), ('adopted', 'Adopted'), ('euthanized', 'Euthanized'), ('aggressive', 'Aggressive'), ('returned', 'Returned')], db_index=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalanimal',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('available', 'Available'), ('requested', 'Requested'), ('pending', 'Pending'), ('adopted', 'Adopted'), ('euthanized', 'Euthanized'), ('aggressive', 'Aggressive'), ('returned', 'Returned')], db_index=True, max_length=20),
        ),
    ]
