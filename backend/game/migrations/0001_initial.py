# Generated by Django 5.0 on 2024-03-14 23:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True, unique_for_date=True)),
                ('type', models.CharField(max_length=50)),
                ('final_score', models.CharField(max_length=50)),
                ('game_tag', models.CharField(max_length=50, null=True)),
                ('loser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gamehistory_user', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gamehistory_winner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Game History',
                'verbose_name_plural': 'Game History',
            },
        ),
        migrations.CreateModel(
            name='GameRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('online', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('user1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Game Room',
                'verbose_name_plural': 'Game Rooms',
            },
        ),
        migrations.CreateModel(
            name='GameStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('tournaments_won', models.IntegerField(default=0)),
                ('tournaments_played', models.IntegerField(default=0)),
                ('game_history', models.ManyToManyField(blank=True, related_name='game_stats', to='game.gamehistory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_stats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Game Stats',
                'verbose_name_plural': 'Game Stats',
            },
        ),
        migrations.CreateModel(
            name='UserChannelName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='game_channel_name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'channel_name')},
            },
        ),
    ]
