# Generated by Django 3.2 on 2021-05-23 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_profile_biometric_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='biometric_data',
            field=models.BinaryField(),
        ),
    ]