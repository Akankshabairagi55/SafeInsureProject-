# Generated by Django 5.0.6 on 2024-08-07 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InsuranceApp', '0003_alter_claim_claim_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurancepolicy',
            name='nominee_of_policy',
        ),
        migrations.AddField(
            model_name='policypurchase',
            name='nominee_of_policy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nominee_detail', to='InsuranceApp.nominee'),
        ),
    ]
