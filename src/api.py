from flask import Flask, Response, jsonify
from flask_restx import Api, Resource
from schedule_service import get_current_schedule, get_schedule_for_tomorrow


app = Flask(__name__)
api = Api(app, version='1.0', title='Electricity Off Lviv Schedule API')

ns = api.namespace('schedule', description='Electricity Off Lviv Schedule API')

@app.route('/')
def ping():
    return 'pong'

@ns.route('/today')
class ScheduleToday(Resource):
    def get(self):
        print('Received request for schedule of today')
        schedule = get_current_schedule()
        print('Got schedule')
        return Response(schedule, mimetype='application/json', content_type='application/json')


@ns.route('/tomorrow')
class ScheduleTomorrow(Resource):
    def get(self):
        print('Received request for schedule of tomorrow')
        schedule = get_schedule_for_tomorrow()
        print('Got schedule for tomorrow')

        if not schedule:
            return jsonify([])

        return Response(schedule, mimetype='application/json', content_type='application/json')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5050)