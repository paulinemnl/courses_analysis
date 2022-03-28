import load
import analysis


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
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
    # Use a breakpoint in the code line below to debug your script.
    # drop_tables()
    create_tables()
    path = "/Users/polinakragel/Study/диплом/Data без архивов"
    load.load_data(path)  # Press ⌘F8 to toggle the breakpoint.
    # analysis.problem_info(1)
    # analysis.materials_info(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
