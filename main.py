import load
import analysis

import models


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


def main():
    # drop_tables()
    # create_tables()
    path = "/Users/polinakragel/Study/diploma/Data"
    # load.load_data(path)
    course_id = 24638
    analysis.problem_info(course_id)
    analysis.materials_info(course_id)


if __name__ == '__main__':
    main()
