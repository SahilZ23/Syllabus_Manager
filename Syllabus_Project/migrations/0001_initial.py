# Generated by Django 3.1.3 on 2020-12-16 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=100)),
                ('courseNumber', models.IntegerField()),
                ('semester', models.CharField(max_length=40)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myName', models.CharField(max_length=40)),
                ('officeLocation', models.CharField(blank=True, max_length=20, null=True)),
                ('officeNumber', models.IntegerField(blank=True, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=40, null=True)),
                ('email', models.CharField(blank=True, max_length=30, null=True)),
                ('day', models.CharField(max_length=50, null=True)),
                ('timeFrom', models.TimeField(null=True, verbose_name='Date Published')),
                ('timeTo', models.TimeField(null=True, verbose_name='DatePublished')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('TA', 'TA'), ('Instructor', 'Instructor'), ('Admin', 'Admin')], max_length=20)),
                ('user_username', models.CharField(max_length=20)),
                ('user_password', models.CharField(max_length=40)),
                ('info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Syllabus_Project.personalinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50)),
                ('timeFrom', models.TimeField(verbose_name='Date Published')),
                ('timeTo', models.TimeField(verbose_name='DatePublished')),
                ('class_room', models.CharField(max_length=40)),
                ('section_number', models.IntegerField(unique=True)),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Syllabus_Project.courses')),
                ('users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Syllabus_Project.users')),
            ],
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policies', models.TextField()),
                ('policy_name', models.CharField(max_length=100)),
                ('policy_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Syllabus_Project.courses')),
                ('policy_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Syllabus_Project.users')),
            ],
        ),
    ]