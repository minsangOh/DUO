# Generated by Django 4.2.7 on 2023-11-23 05:06

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=5)),
                ('last_name', models.CharField(max_length=20)),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('age', models.IntegerField(null=True)),
                ('money', models.IntegerField(null=True)),
                ('salary', models.IntegerField(null=True)),
                ('job', models.CharField(blank=True, choices=[('management', '경영/사무/금융/보험직'), ('engineering', '연구직 및 공학 기술직'), ('education', '교육/법률/사회복지/경찰/소방직 및 군인'), ('health', '보건/의료직'), ('arts', '예술/디자인/방송/스포츠직'), ('service', '미용/여행/숙박/음식/경비/청소직'), ('sales', '영업/판매/운전/운송직'), ('construction', '건설/채굴직'), ('production', '설치/정비/생산직'), ('agriculture', '농림어업직')], max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
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
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marriage_date', models.DateField(blank=True, null=True)),
                ('children_plan', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_fixed_expenses', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('monthly_savings', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.family')),
            ],
        ),
    ]