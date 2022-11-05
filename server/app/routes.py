from app import api
from api.auth import UserLogin
from api.user import UserDb
from api.logs import Logs
from api.report import Report
from api.staffSalary import Salary
from api.history import History
from api.vacation import Vacation
from api.violation import Violation
from api.market import Market
from api.minecraftLogs import MinecraftLogs
from api.activityCheck import ActivityPlayers


api.add_resource(UserLogin, '/api/login')
api.add_resource(UserDb, '/api/users')
api.add_resource(Logs, '/api/logs')
api.add_resource(Salary, '/api/salary')
api.add_resource(Report, '/api/report')
api.add_resource(History, '/api/history')
api.add_resource(Vacation, '/api/vacation')
api.add_resource(Violation, '/api/violation')
api.add_resource(Market, '/api/market')
api.add_resource(ActivityPlayers, '/api/activity')
api.add_resource(MinecraftLogs, '/api/minecraftLogs/<server>')
