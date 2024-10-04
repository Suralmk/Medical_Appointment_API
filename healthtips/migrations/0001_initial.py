# Generated by Django 4.1.11 on 2024-10-02 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import healthtips.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthTips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to=healthtips.models.healthTip_directory_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('order', models.PositiveIntegerField()),
                ('blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to='healthtips.healthtips')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
