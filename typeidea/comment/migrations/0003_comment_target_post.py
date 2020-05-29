# Generated by Django 2.0.7 on 2020-05-29 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_is_md'),
        ('comment', '0002_auto_20200511_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='target_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Post', verbose_name='评论对象'),
        ),
    ]
