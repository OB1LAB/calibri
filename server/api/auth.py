import requests
from app import app
from app.models import User
from flask import jsonify
from validator import validate, error_status
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required,\
    set_refresh_cookies, unset_jwt_cookies, unset_refresh_cookies
from flask_restful import Resource, reqparse
from config import client_id, client_secret, redirect_uri


class UserLogin(Resource):
    def post(self):
        args = parser.parse_args()
        body = {'client_id': client_id, 'client_secret': client_secret, 'code': args['code'],
                'grant_type': 'authorization_code', 'redirect_uri': redirect_uri, 'scope': 'identify'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        code = requests.post('https://discord.com/api/oauth2/token', data=body, headers=headers).json()
        if code.get('access_token'):
            headers = {
                'authorization': 'Bearer {}'.format(code['access_token'])
            }
            ds_id = requests.get('https://discord.com/api/users/@me', headers=headers).json()
            if ds_id.get('id'):
                user = User.query.filter_by(discord_id=ds_id['id']).first()
                if user:
                    access_token = create_access_token(identity=user.name)
                    refresh_token = create_refresh_token(identity=user.name)
                    max_role = user.max_role()
                    data = {
                        'accessToken': access_token,
                        'user': {
                            'name': user.name,
                            'dt': {
                                'name': user.dt_role.name,
                                'lvl': user.dt_role.lvl
                            },
                            'tmrpg': {
                                'name': user.tmrpg_role.name,
                                'lvl': user.tmrpg_role.lvl
                            },
                            'max_role': {
                                'name': max_role.name,
                                'lvl': max_role.lvl
                            }
                        }
                    }
                    resp = jsonify(data)
                    set_refresh_cookies(resp, refresh_token)
                    return resp
        return error_status('User', 'not found')


@app.route('/api/refreshToken', methods=['GET'])
@jwt_required(refresh=True)
def refresh_user_token():
    username = get_jwt_identity()
    user = User.query.filter_by(name=username).first()
    if user:
        access_token = create_access_token(identity=username)
        max_role = user.max_role()
        data = {
            'accessToken': access_token,
            'user': {
                'name': user.name,
                'birthday': user.birthday,
                'balance': user.balance,
                'dt': {
                    'name': user.dt_role.name,
                    'lvl': user.dt_role.lvl,
                    'viewName': user.dt_role.viewName
                },
                'tmrpg': {
                    'name': user.tmrpg_role.name,
                    'lvl': user.tmrpg_role.lvl,
                    'viewName': user.dt_role.viewName
                },
                'max_role': {
                    'name': max_role.name,
                    'lvl': max_role.lvl
                }
            }
        }
        return data
    return error_status('User', 'not found')


@app.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    unset_refresh_cookies(response)
    return response


parser = reqparse.RequestParser()
parser.add_argument('code', required=True, type=validate('code'))
