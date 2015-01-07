def serialize(object):
    result = {}
    for key in object:
    	if key == "id" or key == "LOLTeam" or key == "DOTATeam" or key == "HSTONETeam" or key == "user":
    		pass
    	else:
       	    result[key] = str(object[key])
    return result

def team_serialize(team):
	result = dict()
	for key in team:
		if key == "id" or key == "matchHistory":
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