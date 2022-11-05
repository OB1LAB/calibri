from app import db
from app.models import Server, ServerLogs, Line, Activity, Player
from validator import validate, error_status
from flask_restful import Resource, reqparse
from activity.activity_check import get_activity, log_type
from config import logs_secret


class MinecraftLogs(Resource):
    def get(self, server):
        if server == 'dt':
            server_db = Server.query.filter_by(name='dt').first()
        elif server == 'tmrpg':
            server_db = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Server', 'not found')
        return [log.date for log in server_db.logs]

    def post(self, server):
        if server == 'dt':
            server_db = Server.query.filter_by(name='dt').first()
        elif server == 'tmrpg':
            server_db = Server.query.filter_by(name='tmrpg').first()
        else:
            return error_status('Server', 'not found')
        args = parser.parse_args()
        if args['key'] != logs_secret:
            return error_status('Code', 'not valid')
        add_data, players = [], {}
        for player in server_db.players:
            players[player.name] = player
        logs = server_db.logs.filter_by(date=args['date']).first()
        if not logs:
            logs = ServerLogs(date=args['date'], server_id=server_db.id)
            db.session.add(logs)
            db.session.commit()
        lines = args['logs']
        for line in range(len(logs.lines.all()), len(lines)):
            line_split = lines[line].split()
            add_data.append(Line(line=lines[line], serverLogs_id=logs.id))
            if len(line_split) == 3:
                log_line = log_type(line_split)
                if log_line['type'] == 'join' and log_line['player'] not in players:
                    player = Player(name=log_line['player'], server_id=server_db.id)
                    add_data.append(player)
                    players[log_line['player']] = player
        db.session.add_all(add_data)
        db.session.commit()
        add_data = []
        players_activity = get_activity(server_db, players.keys(), args['date'])
        for player in players_activity:
            player_activity = Activity(date=args['date'], player_id=players[player].id)
            player_activity.local_msg = players_activity[player]['L']
            player_activity.global_msg = players_activity[player]['G']
            player_activity.private_msg = players_activity[player]['PM']
            player_activity.warns = players_activity[player]['Warns']
            player_activity.mutes = players_activity[player]['Mutes']
            player_activity.kicks = players_activity[player]['Kicks']
            player_activity.bans = players_activity[player]['Bans']
            player_activity.online = players_activity[player]['online_time']
            player_activity.online_vanish = players_activity[player]['vanish_time']
            players[player].online = players_activity[player]['Online']
            players[player].vanish = players_activity[player]['Vanish']
            add_data.append(player_activity)
        db.session.add_all(add_data)
        db.session.commit()
        return "successfully"


parser = reqparse.RequestParser()
parser.add_argument('key', type=validate('code'), location="form")
parser.add_argument('logs', required=True, type=str, action='append', location="form")
parser.add_argument('date', required=True, type=str, location="form")
