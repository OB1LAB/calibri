from app.models import User, AppLogs
from validator import error_status
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource


class Logs(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.filter_by(name=get_jwt_identity()).first()
        if current_user.max_role().lvl < 5:
            return error_status('Permissions', 'You don\'t have permissions')
        logs = [f"[{log.date.strftime('%d-%m-%Y %H:%M:%S')}] {log.log}" for log in AppLogs.query.all()]
        logs.reverse()
        return logs
