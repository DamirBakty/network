# Generated by Django 4.1.7 on 2023-04-16 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0002_alter_comment_post_alter_commentlike_post_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="commentlike", old_name="post", new_name="comment",
        ),
    ]