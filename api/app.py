from flask import Flask
from celery import Celery

app = Flask(__name__)
simple_app = Celery('simple_worker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    #                        queue name in task folder.function name
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    app.logger.info(r.backend)
    return r.id


@app.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)