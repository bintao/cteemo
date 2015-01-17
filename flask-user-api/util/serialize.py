def serialize(object):
	result = {}
	for key in object:
		if key == "DOTATeam" or key == "HSTONETeam" or key == "user" or object[key] is None:
			pass
		elif key == "LOLTeam" and object['LOLTeam'] is not None:
			result[key] = object[key].teamName
			result['LOLTeamID'] = str(object[key].id)
		else:
			result[key] = str(object[key])
	return result

def team_serialize(team):
	result = dict()
	for key in team:
		if key == "matchHistory" or team[key] is None:
			pass
		elif key == "captain":
			result['captain'] = profile_search_serialize([team[key]]) 
		elif key == "members":
			result['members'] = profile_search_serialize(team[key])
		else:
			result[key] = str(team[key])
	return result

def team_search_serialize(teams):
	result = list()
	for team in teams:
		result.append({
			'teamID' : str(team.id),
			'teamName' : team.teamName,
			'teamIcon' : team.teamIcon,
			'captain' : team.captain.username,
			'school' : team.school
			})
	return result

def profile_serialize(profiles):
	username,icons,userID = list(),list(),list()
	for profile in profiles:
		username.append(profile.username)
		icons.append(profile.profile_icon)
		userID.append(str(profile.user.id))
	return username,icons,userID

def profile_search_serialize(profiles):
	result = list()
	for profile in profiles:
		result.append({
			'profile_id': str(profile.id),
			'username': profile.username,
			'profile_icon': profile.profile_icon,
			'school': profile.school
			})
	return result

def friends_list_serialize(friends_list):
	return profile_search_serialize(friends_list)

def tournament_serialize(tournament):
	result = dict()
	for key in tournament:
		if key == 'creator':
			result[key] = tournament[key].username
		elif key == 'rounds':
			result[key] = round_serialize(tournament[key])
		else:
			result[key] = str(tournament[key])
	return result

def requests_list_serialize(requests_list):
	return profile_search_serialize(requests_list)

def round_serialize(rounds):
	result = list()
	for round in rounds:
		result.append({
			'round' : round.roundName,
			'time' : str(round.startTime),
			'bestOfN' : round.bestOfN
			})
	return result

def post_user_profile_serialize(profile):
	return {
		'id': str(profile.id),
		'username': profile.username,
		'profile_icon': profile.profile_icon,
	}


def posts_list_serialize(posts):
	result = []
	for post in posts:
		result.append({
			'user_profile': post_user_profile_serialize(post.user_profile),
			'date': post.date.strftime("%B %d, %Y %I:%M%p"),
			'content': post.content
		})
	return result

def tournament_search_serialize(tournaments):
	result = list()
	for tournament in tournaments:
		result.append(tournament_serialize(tournament))
	return result

def match_serialize(match):
	result = dict()
	for key in match:
		if key == 'teams':
			result[key] = team_search_serialize(match[key])
		elif key == 'tournament':
			pass
		elif key == 'round':
			result[key] = match[key].roundName
		else:
			try:
				result[key] = str(match[key])
			except:
				result[key] = match[key]
	return result