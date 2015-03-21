from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from api.rongcloudAPI import rongRefresh
from util.userAuth import auth_required
from util.serialize import serialize, profile_search_serialize
from util.exception import InvalidUsage
from mongoengine.queryset import Q
import boto
import os


profileParser = reqparse.RequestParser()
profileParser.add_argument('username', type=str)
profileParser.add_argument('school', type=str)
profileParser.add_argument('intro', type=str)
profileParser.add_argument('lolID', type=str)
profileParser.add_argument('dotaID', type=str)
profileParser.add_argument('hstoneID', type=str)
profileParser.add_argument('profileID', type=int)
profileParser.add_argument('page', type=int)

class ProfileAPI(Resource):
    @auth_required
    def get(self, user_id):
        # load profile 
        profile =  Profile.objects(user=user_id).first()
        if profile is None:
        	return {}

        return serialize(profile)

    @auth_required
    def post(self, user_id):
    	args = profileParser.parse_args()
        username = args['username']
        school = args['school']
        intro = args['intro']
        lolID = args['lolID']
        dotaID = args['dotaID']
        hstoneID = args['hstoneID']

        profile = Profile.objects(user=user_id).first()
        if profile is None:
            profile = Profile(user=user_id)
        profile.username = username
        profile.school = school
        profile.intro = intro
        profile.lolID = lolID
        profile.dotaID = dotaID
        profile.hstoneID = hstoneID
        profile.save()
        
        rongRefresh(profile.id)

        return serialize(profile)

class ProfileIconAPI(Resource):
    @auth_required
    def post(self, user_id):
        uploaded_file = request.files['upload']
        filename = "_".join([user_id, uploaded_file.filename])

        conn = boto.connect_s3('AKIAJAQHGWIZDOAEQ65A', 'FpmnFv/jte9ral/iXHtL8cDUnuKXAgAqp9aXVQMI')
        bucket = conn.get_bucket('profile-icon')
        key = bucket.new_key(filename)
        key.set_contents_from_file(uploaded_file)

        profile = Profile.objects(user=user_id).first()
        if profile is None:
            profile = Profile(user=user_id, profile_icon='https://s3-us-west-2.amazonaws.com/profile-icon/%s' %filename)
            profile.save()
        else:
            profile.profile_icon = 'https://s3-us-west-2.amazonaws.com/profile-icon/%s' %filename
            profile.save()

        rongRefresh(profile.id)
        
        return serialize(profile)

class FindProfileAPI(Resource):
    @auth_required
    def get(self, user_id):
        args = profileParser.parse_args()
        username = args['username']
        school = args['school']
        page = args['page']
        if (username is None and school is None):
            raise InvalidUsage('No argument provided')
        if page is None:
            page = 0

        profiles = Profile.objects.only('username', 'profile_icon', 'school')
        if username is not None:
            profiles = profiles.filter(username__icontains=username)
        if school is not None:
            profiles = profiles.filter(school=school)

        return profile_search_serialize(profiles[10*page:10*(page+1)])

class ViewProfileAPI(Resource):
    def get(self, profileID):
        profile = Profile.objects(id=profileID).first()
        if profile is None:
            raise InvalidUsage('Profile not found',404)

        return serialize(profile)