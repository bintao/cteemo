def serialize(object):
    result = {}
    for key in object:
    	if key == "id" or key == "LOLTeam" or key == "DOTATeam" or key == "HSTONETeam":
    		pass
    	elif key == "user":
    		result[key] = str(object[key].id)
    	else:
       	    result[key] = str(object[key])
    return result

def team_serialize(team):
	result = dict()
	for key in team:
		if key == "id" or key == "matchHistory":
			pass
		elif key == "captain":
			result['captain'],result['captain_icon'],result['captain_id'] = profile_serialize([team[key]]) 
		elif key == "members":
			result['members'],result['members_icon'],result['members_id'] = profile_serialize(team[key])
		else:
			result[key] = str(team[key])
	return result

def profile_serialize(profiles):
	username,icons,userID = list(),list(),list()
	for profile in profiles:
		username.append(profile.username)
		icons.append(profile.profile_icon)
		userID.append(str(profile.user.id))
	return username,icons,userID

def profile_search_serialize(profiles):
	result = dict()
	result['username'],result['icons'],result['userID'] = profile_serialize(profiles)
	return result