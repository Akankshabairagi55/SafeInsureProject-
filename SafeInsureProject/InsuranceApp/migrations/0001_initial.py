# Generated by Django 5.0.6 on 2024-08-01 18:25

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_company', models.CharField(max_length=100)),
                ('headquarters', models.CharField(blank=True, max_length=200, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('company_address', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nominee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_nominee', models.CharField(max_length=100)),
                ('relation', models.CharField(blank=True, max_length=15, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InsurancePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types_of_insurance', models.CharField(choices=[('health', 'Health Insurance'), ('car', 'Car Insurance'), ('life', 'Life Insurance'), ('home', 'Home Insurance'), ('term', 'Term Insurance')], max_length=50)),
                ('policy_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('premium_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('coverage_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_age', models.IntegerField(blank=True, null=True)),
                ('max_age', models.IntegerField(blank=True, null=True)),
                ('maturity_period', models.CharField(blank=True, max_length=50, null=True)),
                ('waiting_period', models.CharField(blank=True, max_length=50, null=True)),
                ('expiry_period', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_policies', to='InsuranceApp.company')),
                ('nominee_of_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominee_detail', to='InsuranceApp.nominee')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_customer', models.CharField(max_length=200)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('nominee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='InsuranceApp.nominee')),
            ],
        ),
        migrations.CreateModel(
            name='PolicyPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired')], default='active', max_length=50)),
                ('policy_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='InsuranceApp.customer')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_policies', to='InsuranceApp.insurancepolicy')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer')], max_length=50)),
                ('policy_purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='InsuranceApp.policypurchase')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='policies',
            field=models.ManyToManyField(through='InsuranceApp.PolicyPurchase', to='InsuranceApp.insurancepolicy'),
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('claim_date', models.DateTimeField(auto_now_add=True)),
                ('claim_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('claim_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('policy_purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='InsuranceApp.policypurchase')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_customer', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
