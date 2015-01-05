#serialize
def serialize(team):
    if team is None:
        return None
    result,members,icons = dict(),list(),list()
    for key in team:
        if key != "id" and key != 'team_members' and key != 'owner':
            result[key] = str(team[key])
    result['owner'] = team.owner.user_email
    for profile in team.team_members:
        members.append(profile.username)
        icons.append(profile.profile_icon)
    result['members'] = members
    result['icons'] = icons
    return result