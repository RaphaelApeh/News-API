# Generated by Django 5.1.4 on 2024-12-25 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_alter_post_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="post_images"),
        ),
    ]
