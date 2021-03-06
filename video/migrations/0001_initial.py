# Generated by Django 2.1.7 on 2019-04-02 12:37

from django.conf import settings
from django.db import migrations, models
import video.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '分类名称',
                'verbose_name_plural': '分类名称',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_date', models.DateTimeField(auto_now_add=True, verbose_name='观看时间')),
                ('user', models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '观看历史',
                'verbose_name_plural': '观看历史',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, verbose_name='标签名')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('user', models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '点赞',
                'verbose_name_plural': '点赞',
            },
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='专辑名称')),
            ],
            options={
                'verbose_name': '专辑',
                'verbose_name_plural': '专辑',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='视频名称')),
                ('link', models.FileField(upload_to=video.models.get_video_path, verbose_name='视频链接')),
                ('img', models.ImageField(upload_to=video.models.get_img_path, verbose_name='视频图片')),
                ('passwd', models.CharField(blank=True, max_length=10, null=True, verbose_name='播放密码')),
                ('introduce', models.TextField(verbose_name='视频介绍')),
                ('hour', models.CharField(max_length=10, verbose_name='视频时长')),
                ('views', models.IntegerField(default=0, verbose_name='观看次数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='创建日期')),
                ('status', models.CharField(choices=[('上线', '上线'), ('下线', '下线')], default='上线', max_length=10, verbose_name='状态')),
                ('cate', models.ForeignKey(on_delete=True, to='video.Cate', verbose_name='视频分类')),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频',
            },
        ),
        migrations.AddField(
            model_name='set',
            name='video',
            field=models.ForeignKey(on_delete=True, to='video.Video', verbose_name='视频名称'),
        ),
        migrations.AddField(
            model_name='likes',
            name='video',
            field=models.ForeignKey(on_delete=True, to='video.Video', verbose_name='视频'),
        ),
        migrations.AddField(
            model_name='label',
            name='video',
            field=models.ForeignKey(on_delete=True, to='video.Video', verbose_name='视频'),
        ),
        migrations.AddField(
            model_name='history',
            name='video',
            field=models.ForeignKey(on_delete=True, to='video.Video'),
        ),
    ]
