import pandas as pd

import load
import analysis
import models
import clustering


def create_tables():
    models.User.create_table()
    models.Course.create_table()
    models.VideoInteractionEvent.create_table()
    models.BookEvent.create_table()
    models.NavigationEvent.create_table()
    models.ProblemInteractionEvent.create_table()
    models.EnrollmentEvent.create_table()
    models.CertificateEvents.create_table()


def drop_tables():
    m = (models.User, models.Course, models.VideoInteractionEvent, models.BookEvent, models.NavigationEvent,
         models.ProblemInteractionEvent, models.EnrollmentEvent, models.CertificateEvents)
    models.db.drop_tables(m)


def get_data(course_id):
    query_problem = models.ProblemInteractionEvent.select().where(models.ProblemInteractionEvent.course_id == course_id)
    query_book = models.BookEvent.select().where(models.BookEvent.course_id == course_id)
    query_video = models.VideoInteractionEvent.select().where((models.VideoInteractionEvent.course_id == course_id) &
                                                              (models.VideoInteractionEvent.type_event == 'play_video'))
    df_problem = pd.DataFrame(query_problem.dicts())
    df_book = pd.DataFrame(query_book.dicts())
    df_video = pd.DataFrame(query_video.dicts())
    return df_problem, df_book, df_video


def main():
    course_id = 19618
    df_problem, df_book, df_video = get_data(course_id)
    clustering.clustering(df_problem, df_book, df_video)
    # analysis.course_info(df_problem, df_book, df_video)


if __name__ == '__main__':
    main()
