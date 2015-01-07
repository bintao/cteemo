from flask import request, abort
from flask.ext.restful import Resource, reqparse
from model.profile import Profile
from userAuth import auth_required
from serialize import serialize, profile_search_serialize
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

        return serialize(profile)

class findProfileAPI(Resource):
    @auth_required
    def get(self, user_id):
        args = profileParser.parse_args()
        username = args['username']
        school = args['school']
        if username is None and school is None:
            abort(400)
        elif username is None:
            profiles = Profile.objects(school=school)
        elif school is None:
            profiles = Profile.objects(username__icontains=username)
        else:
            profiles = Profile.objects(Q(username__icontains=username) & Q(school=school))
        return profile_search_serialize(profiles[:5])