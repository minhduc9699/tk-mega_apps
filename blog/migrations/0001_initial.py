# Generated by Django 2.0.5 on 2018-12-05 03:49

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeOil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Oil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('tag', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('question', ckeditor.fields.RichTextField()),
                ('anwser', ckeditor.fields.RichTextField()),
                ('resource', models.URLField(blank=True, default='', max_length=400)),
                ('state', models.CharField(choices=[('approve', 'Approve'), ('approve with edit', 'Approve With edit'), ('not approve', 'Not approve')], default='not approve', max_length=250)),
                ('kudo', models.FloatField(default=0)),
                ('on_payroll', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('viewer', 'Viewer'), ('contributor', 'Contributor'), ('editor', 'Editor'), ('manager', 'Manager')], default='viewer', max_length=255)),
                ('kudo', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='oil',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to='blog.UserProfile'),
        ),
        migrations.AddField(
            model_name='oil',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editor', to='blog.UserProfile'),
        ),
        migrations.AddField(
            model_name='likeoil',
            name='oil_like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oil_like', to='blog.Oil'),
        ),
        migrations.AddField(
            model_name='likeoil',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to='blog.UserProfile'),
        ),
    ]
