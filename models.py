from peewee import *


db = PostgresqlDatabase('openedu', host='localhost', port=5432, user='postgres', password='7003')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(column_name='id', primary_key=True)
    username = TextField(column_name='username', null=False)

    class Meta:
        db_table = 'users'


class Course(BaseModel):
    course_id = AutoField(column_name='id')
    course_name = TextField(column_name='course_name', unique=True, null=False)

    class Meta:
        db_table = 'courses'


class VideoInteractionEvent(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, field='user_id')
    course_id = ForeignKeyField(Course, field='course_id')
    time_event = DateTimeField(column_name='time_event', null=False)
    type_event = TextField(column_name='type_event', null=False, constraints=[Check(
        'type_event = \'pause_video\' or type_event = \'play_video\' or type_event = \'seek_video\' or type_event = '
        '\'speed_change_video\'')])
    video_id = TextField(column_name='video_id', null=False)
    current_time_video = DoubleField(column_name='current_time_video', null=True)
    new_time = DoubleField(column_name='new_time', null=True)
    old_time = DoubleField(column_name='old_time', null=True)
    new_speed = DoubleField(column_name='new_speed', null=True)
    old_speed = DoubleField(column_name='old_speed', null=True)

    class Meta:
        db_table = 'video_interaction_events'


class BookEvent(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, field='user_id')
    course_id = ForeignKeyField(Course, field='course_id')
    time_event = DateTimeField(column_name='time_event', null=False)
    chapter = TextField(column_name='chapter', null=False)
    type_event = TextField(column_name='type_event', null=False, constraints=[
        Check('type_event = \'gotopage\' or type_event = \'prevpage\' or type_event = \'nextpage\'')])
    new_page = IntegerField(column_name='new_page', null=False)
    old_page = IntegerField(column_name='old_page', null=True)

    class Meta:
        db_table = 'book_interaction_events'


class NavigationEvent(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, field='user_id')
    course_id = ForeignKeyField(Course, field='course_id')
    time_event = DateTimeField(column_name='time_event', null=False)
    type_event = TextField(column_name='type_event', null=False, constraints=[
        Check('type_event = \'seq_goto\' or type_event = \'seq_next\' or type_event = \'seq_prev\'')])
    seq_id = TextField(column_name='seq_id', null=False)
    new_page = IntegerField(column_name='new_page', null=False)
    old_page = IntegerField(column_name='old_page', null=False)

    class Meta:
        db_table = 'navigation_events'


class ProblemInteractionEvent(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, field='user_id')
    course_id = ForeignKeyField(Course, field='course_id')
    time_event = DateTimeField(column_name='time_event', null=False)
    problem_id = TextField(column_name='problem_id', null=False)
    attempts = IntegerField(column_name='attempts', null=False)
    grade = IntegerField(column_name='grade', null=False)
    max_grade = IntegerField(column_name='max_grade', null=False)
    success = TextField(column_name='success', null=False,
                        constraints=[Check('success = \'correct\' or success = \'incorrect\'')])

    class Meta:
        db_table = 'problem_interaction_events'


class EnrollmentEvent(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, field='user_id')
    course_id = ForeignKeyField(Course, field='course_id')
    time_event = DateTimeField(column_name='time_event', null=False)

    class Meta:
        db_table = 'enrollment_events'


class CertificateEvents(BaseModel):
    id = AutoField(column_name='id')
    user_id = ForeignKeyField(User, field='user_id')
    course_id = ForeignKeyField(Course, field='course_id')
    time_event = DateTimeField(column_name='time_event', null=False)

    class Meta:
        db_table = 'certificate_events'
