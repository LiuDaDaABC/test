from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# passwd = models.CharField(verbose_name='播放密码',max_length=10,null=True,blank=True)
# hour = models.CharField(verbose_name="视频时长",max_length=10)
# status = models.CharField(verbose_name='状态',choices=(('上线','上线'),('下线','下线')),max_length=10,default="上线")


# 分类
class Cate(models.Model):
    name = models.CharField(verbose_name="分类名称",max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

def get_video_path(instance, filename):
    return 'video/{0}/{1}'.format(instance.name,filename)

def get_img_path(instance, filename):
    return 'video_img/{0}/{1}'.format(instance.name,filename)

# 视频
class Video(models.Model):
    name = models.CharField(verbose_name='视频名称',max_length=20)
    link = models.FileField(verbose_name='视频链接',upload_to=get_video_path)
    img = models.ImageField(verbose_name='视频图片',upload_to=get_img_path)
    introduce = models.TextField(verbose_name="视频介绍")
    cate = models.ForeignKey(Cate,verbose_name='视频分类',on_delete=True)
    views = models.IntegerField(verbose_name='观看次数',default=0)
    like = models.IntegerField(verbose_name='观看次数',default=0)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    create_date = models.DateField(verbose_name='创建日期',auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

# 标签
class Label(models.Model):
    video = models.ForeignKey(Video,verbose_name="视频",on_delete=True)
    label = models.CharField(verbose_name="标签名",max_length=10)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

# 专辑
class Set(models.Model):
    name = models.CharField(verbose_name="专辑名称",max_length=20)
    video = models.ForeignKey(Video,verbose_name='视频名称',on_delete=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '专辑'
        verbose_name_plural = verbose_name

# 点赞
class Likes(models.Model):
    video = models.ForeignKey(Video,verbose_name='视频',on_delete=True)
    user = models.ForeignKey(User,verbose_name='用户',on_delete=True)
    time = models.DateTimeField(verbose_name='时间',auto_now_add=True)

    def __str__(self):
        return str(self.video)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name

# 历史
class History(models.Model):
    video = models.ForeignKey(Video,on_delete=True)
    user = models.ForeignKey(User,on_delete=True)
    view_date = models.DateTimeField(verbose_name='观看时间',auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '观看历史'
        verbose_name_plural = verbose_name