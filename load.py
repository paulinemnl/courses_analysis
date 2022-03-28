import os
import glob
import json

import models


@models.db.atomic()
def create_user(data):
    try:
        return models.User.create(user_id=data['context']['user_id'], username=data['username'])
    except models.IntegrityError:
        pass


@models.db.atomic()
def create_course(data):
    try:
        return models.Course.create(course_name=data['context']['course_id'])
    except models.IntegrityError:
        pass


@models.db.atomic()
def create_video_play_pause(data):
    data_event = json.loads(data['event'])
    return models.VideoInteractionEvent.create(user_id=data['context']['user_id'],
                                               course_id=models.Course.select().where(
                                                   models.Course.course_name == data['context'][
                                                       'course_id']).get().course_id,
                                               type_event=data['event_type'], time_event=data['time'],
                                               video_id=data_event['id'],
                                               current_time_video=data_event['currentTime'])


@models.db.atomic()
def create_video_seek(data):
    data_event = json.loads(data['event'])
    return models.VideoInteractionEvent.create(user_id=data['context']['user_id'],
                                               course_id=models.Course.select().where(
                                                   models.Course.course_name == data['context'][
                                                       'course_id']).get().course_id,
                                               type_event=data['event_type'], time_event=data['time'],
                                               video_id=data_event['id'], new_time=data_event['new_time'],
                                               old_time=data_event['old_time'])


@models.db.atomic()
def create_video_speed(data):
    data_event = json.loads(data['event'])
    return models.VideoInteractionEvent.create(user_id=data['context']['user_id'],
                                               course_id=models.Course.select().where(
                                                   models.Course.course_name == data['context'][
                                                       'course_id']).get().course_id,
                                               type_event=data['event_type'], time_event=data['time'],
                                               video_id=data_event['id'],
                                               current_time_video=data_event['current_time'],
                                               new_speed=data_event['new_speed'],
                                               old_speed=data_event['old_speed'])


@models.db.atomic()
def create_book(data):
    data_event = json.loads(data['event'])
    old_page = None
    if data_event['type'] == 'gotopage':
        old_page = data_event['old']
    return models.BookEvent.create(user_id=data['context']['user_id'],
                                   course_id=models.Course.select().where(
                                       models.Course.course_name == data['context'][
                                           'course_id']).get().course_id,
                                   type_event=data_event['type'], time_event=data['time'],
                                   chapter=data_event['chapter'],
                                   new_page=data_event['new'], old_page=old_page)


@models.db.atomic()
def create_navigation(data):
    data_event = json.loads(data['event'])
    return models.NavigationEvent.create(user_id=data['context']['user_id'],
                                         course_id=models.Course.select().where(
                                             models.Course.course_name == data['context'][
                                                 'course_id']).get().course_id,
                                         type_event=data['event_type'], time_event=data['time'],
                                         seq_id=data_event['id'],
                                         new_page=data_event['new'], old_page=data_event['old'])


@models.db.atomic()
def create_problem(data):
    return models.ProblemInteractionEvent.create(user_id=data['context']['user_id'],
                                                 course_id=models.Course.select().where(
                                                     models.Course.course_name == data['context'][
                                                         'course_id']).get().course_id,
                                                 time_event=data['time'], problem_id=data['event']['problem_id'],
                                                 attempts=data['event']['attempts'], grade=data['event']['grade'],
                                                 max_grade=data['event']['max_grade'], success=data['event']['success'])


@models.db.atomic()
def create_certificate(data):
    return models.CertificateEvents.create(user_id=data['context']['user_id'],
                                           course_id=models.Course.select().where(
                                               models.Course.course_name == data['context'][
                                                   'course_id']).get().course_id, time_event=data['time'])


@models.db.atomic()
def create_enrollment(data):
    return models.EnrollmentEvent.create(user_id=data['context']['user_id'],
                                         course_id=models.Course.select().where(
                                             models.Course.course_name == data['context'][
                                                 'course_id']).get().course_id, time_event=data['time'])


def load_data(path):
    os.chdir(path)
    all_log_files = glob.glob('*.log')
    for entry in all_log_files:
        with open(entry, 'rt') as file:
            for line in file:
                data = json.loads(line)
                try:
                    user_id = data['context']['user_id']
                except KeyError:
                    continue
                if user_id is not None:
                    match data['event_type']:
                        case "play_video" | "pause_video":
                            create_user(data)
                            create_course(data)
                            create_video_play_pause(data)
                        case "seek_video":
                            create_user(data)
                            create_course(data)
                            create_video_seek(data)
                        case "speed_change_video":
                            create_user(data)
                            create_course(data)
                            create_video_speed(data)
                        case "book":
                            create_user(data)
                            create_course(data)
                            create_book(data)
                        case "seq_goto" | "seq_next" | "seq_prev":
                            create_user(data)
                            create_course(data)
                            create_navigation(data)
                        case "problem_check":
                            if data['event_source'] == 'server':
                                create_user(data)
                                create_course(data)
                                create_problem(data)
                            else:
                                continue
                        case "edx.course.enrollment.activated":
                            create_user(data)
                            create_course(data)
                            create_enrollment(data)
                        case "edx.certificate.created":
                            create_user(data)
                            create_course(data)
                            create_certificate(data)
