# Generated by Django 3.1.1 on 2020-09-06 15:09

import backend_django.utils
import django.core.validators
from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255, null=True)),
                ('identifier', models.CharField(db_index=True, max_length=255, null=True)),
                ('domain', models.CharField(db_index=True, max_length=255, null=True)),
                ('year_founded', models.CharField(db_index=True, max_length=8, null=True)),
                ('description', models.TextField(null=True)),
                ('address_2', models.CharField(max_length=500, null=True)),
                ('address', models.CharField(max_length=500, null=True)),
                ('city', models.CharField(db_index=True, max_length=255, null=True)),
                ('state', models.CharField(db_index=True, max_length=255, null=True)),
                ('postal', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(db_index=True, max_length=255, null=True)),
                ('industry', models.CharField(db_index=True, max_length=255, null=True)),
                ('google_industry', models.CharField(db_index=True, max_length=255, null=True)),
                ('current_equity', models.CharField(max_length=255, null=True)),
                ('best_equity', models.CharField(max_length=255, null=True)),
                ('categories', models.CharField(db_index=True, max_length=255, null=True)),
                ('bounce_rate', models.FloatField(null=True)),
                ('daily_time', models.CharField(max_length=200, null=True)),
                ('page_views', models.FloatField(null=True)),
                ('rank', models.BigIntegerField(null=True)),
                ('is_public', models.BooleanField(null=True)),
                ('naics', models.CharField(max_length=200, null=True)),
                ('sic', models.CharField(max_length=200, null=True)),
                ('fb_page', models.CharField(max_length=1000, null=True)),
                ('twitter_handle', models.CharField(max_length=1000, null=True)),
                ('li_page', models.CharField(max_length=1000, null=True)),
                ('t_money_raised', models.CharField(max_length=200, null=True)),
                ('competitors', django_mysql.models.JSONField(default=backend_django.utils.defaultCompetitorValues)),
                ('g1', models.BooleanField(null=True)),
                ('g2', models.BooleanField(null=True)),
                ('g3', models.BooleanField(null=True)),
                ('g4', models.BooleanField(null=True)),
                ('g5', models.BooleanField(null=True)),
                ('g6', models.BooleanField(null=True)),
                ('g7', models.BooleanField(null=True)),
                ('g8', models.BooleanField(null=True)),
                ('g_true', models.IntegerField(db_index=True, default=0, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)])),
                ('g_false', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)])),
                ('g_total', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)])),
                ('annual_revenue', models.FloatField(db_index=True, null=True)),
                ('num_emp', models.BigIntegerField(db_index=True, null=True)),
                ('churn_employees', models.FloatField(null=True)),
                ('churn_rate', models.FloatField(null=True)),
                ('revenue_per_employee', models.FloatField(null=True)),
                ('revenue_variance', models.FloatField(null=True)),
                ('a_revenue_since_founding', models.FloatField(null=True)),
                ('revenue_growth_first_to_current', models.FloatField(null=True)),
                ('emp_growth_first_to_current', models.FloatField(null=True)),
                ('current_employees', models.IntegerField(null=True)),
                ('revenue_quarter_chart', django_mysql.models.JSONField(default=backend_django.utils.defaultValues)),
                ('employee_quarter_chart', django_mysql.models.JSONField(default=backend_django.utils.defaultValues)),
                ('is_premium', models.BooleanField(db_index=True, default=False)),
                ('is_disabled', models.BooleanField(db_index=True, default=False)),
                ('test', models.IntegerField(null=True)),
                ('last_modified', django_mysql.models.JSONField(default=backend_django.utils.defaultValues)),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip_addr', models.GenericIPAddressField(db_index=True)),
                ('state', models.CharField(db_index=True, max_length=60, null=True)),
                ('city', models.CharField(db_index=True, max_length=600, null=True)),
                ('expiration', models.DateTimeField(default=backend_django.utils.returnEpirationDate)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('arg', models.TextField(null=True)),
            ],
        ),
    ]
