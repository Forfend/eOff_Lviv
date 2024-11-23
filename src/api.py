from flask import Flask, Response, jsonify
from flask_restx import Api, Resource
from schedule_service import get_current_schedule, get_schedule_for_tomorrow
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app, version='1.0', title='Electricity Off Lviv Schedule API')

ns = api.namespace('schedule', description='Electricity Off Lviv Schedule API')

@ns.route('/ping')
class HealthCheck(Resource):
    def get(self):
        return 'pong'

@ns.route('/today')
class ScheduleToday(Resource):
    def get(self):
        logger.info('Received request for schedule of today')
        schedule = get_current_schedule()
        logger.info('Got schedule')
        return Response(schedule, mimetype='application/json', content_type='application/json')


@ns.route('/tomorrow')
class ScheduleTomorrow(Resource):
    def get(self):
        logger.info('Received request for schedule of tomorrow')
        schedule = get_schedule_for_tomorrow()
        logger.info('Got schedule for tomorrow')

        if not schedule:
            return jsonify([])

        return Response(schedule, mimetype='application/json', content_type='application/json')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)