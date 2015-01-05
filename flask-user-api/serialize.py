def serialize(object):
    result = {}
    for key in object:
    	if key == "id" or key == "user" or key == "LOLTeam" or key == "DOTATeam" or key == "HSTONETeam":
    		pass
    	else:
       	    result[key] = str(object[key])
    return result

def team_serialize(team):
	result = dict()
	for key in team:
		if key == "id" or key == "meta" or key == "matchHistory":
			pass
		elif key == "captain":
			result['captain'],result['captain_icon'] = profile_serialize([team[key]]) 
		elif key == "members":
			result['members'],result['members_icon'] = profile_serialize(team[key])
		else:
			result[key] = str(team[key])
	return result

def profile_serialize(profiles):
	username,icons = list(),list()
	for profile in profiles:
		username.append(profile.username)
		icons.append(profile.profile_icon)
	return username,icons