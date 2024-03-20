from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from user_api.models import AppUser
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

import string
import random
import json
import logging
from django.http import JsonResponse

def get_user_from_session(session_key):
	session = Session.objects.get(session_key=session_key)
	user_id = session.get_decoded().get('_auth_user_id')
	user = User.objects.get(id=user_id)
	return user

logger = logging.getLogger(__name__)

# Then, instead of print, use logger.info (or logger.debug, logger.warning, etc.)

def generate_random_lobby_name(length=10):
	# Generate a random string of the given length
	lobby_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
	return lobby_name 


def prepare_room(room_name):
	"""
	Helper function to get the game room object by room name.
	"""
	game_room = GameRoom.objects.filter(name=room_name).first()
	return game_room


def room(request, room_name):
	# Get or create the game room for the users
	room_obj = prepare_room(room_name)
	if not room_obj:
		room_name = "asdfasdf"
		room_obj = GameRoom.objects.create(name=room_name)
	
	session_id = request.COOKIES.get('sessionid')
	if session_id:
		user = get_user_from_session(session_id)
	else:
		# Handle the case when session_id is None
		# You can return an error response or a default user
		return JsonResponse({'error': 'No session id in cookies'}, status=400)

	# Prepare data for rendering, will be passed to template
	context = {
		"room_name": room_obj.name,
		"sender": user.id,
		# "user1": room_obj.user1,
		# "user2": room_obj.user2.id,
		# "player0": room_obj.user1.username,
		# "player1": room_obj.user2.username,
	}
	# logger.info("-----------------------------------------")
	# logger.info(f"{context['lobby_name']}, {context['sender']}, {context['user1']}, {context['user2']}, {context['player0']}, {context['player1']}")
	# logger.info("-----------------------------------------")

	return JsonResponse(context)


def game_ending(request):
	# Get parameters from request
	game_info = request.GET.get('gameinfo', None)
	game_tag = request.GET.get('gametag', None)
	lobby_name = request.GET.get('roomname', None)
	# Parse game_info string from request
	users = game_info.split('|')
	winner_id = users[0].split(':')[0]
	winner_score = users[0].split(':')[1]
	loser_id = users[1].split(':')[0]
	loser_score = users[1].split(':')[1]
	# Get User objects
	winner = get_object_or_404(AppUser, id=winner_id)
	loser = get_object_or_404(AppUser, id=loser_id)
	if winner.game_stats is None:
		winner.game_stats = GameStats.objects.create(user=winner)
		winner.save()
	if loser.game_stats is None:
		loser.game_stats = GameStats.objects.create(user=loser)
		loser.save()
	# logger.info("-----------------------------------------")
	# logger.info(f"{winner}, {loser}, {winner_score}, {loser_score}, {game_tag}, {lobby_name}")
	# logger.info("-----------------------------------------")

	# Set up variables to populate entry in GameHistory table
	final_score = f"{winner_score}:{loser_score}"
	# Check if the entry already exists
	existing_entry = GameHistory.objects.filter(game_tag=game_tag).first()
	if not existing_entry:
		# Entry does not exist, create a new one
		game_history = GameHistory(type="1v1", winner=winner, loser=loser, final_score=final_score, game_tag=game_tag)
		game_history.save()
		winner.game_stats.add_game_history(game_history)
		loser.game_stats.add_game_history(game_history)
		winner.game_stats.add_win()
		loser.game_stats.add_loss()
	# Return to game room
	room_obj = GameRoom.objects.filter(name=lobby_name).first()
	other_user = room_obj.user1.username if room_obj.user1.username != request.user.username else room_obj.user2.username
	# return game info to the room

	return JsonResponse(
		{
			"winner": winner.username,
			"loser": loser.username,
			"final_score": final_score,
			"other_user": other_user,
		}
	)
