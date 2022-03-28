import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math

import models

pd.set_option('display.max_columns', None)


def percent_compl_tasks(df):
    df_user_percent = pd.DataFrame(columns=['user_id', 'percent'])
    amount_of_problem = pd.unique(df['problem_id']).shape[0]
    for i in pd.unique(df['user_id']):
        df_user_percent.loc[len(df_user_percent)] = [i, df[(df.user_id == i) & (df.success == 'correct')].shape[
            0] / amount_of_problem * 100]
    df_user_percent = df_user_percent[(df_user_percent.percent != 0) & (df_user_percent.percent != 100)]
    plt.hist(df_user_percent['percent'], range=(0, 100))
    plt.locator_params(axis='y', integer=True)
    plt.title('Процент выполненных заданий')
    plt.ylabel('Количество учащихся')
    plt.xlabel('%')
    plt.show()


def amount_success_tasks(df):
    df = df.rename(columns={'id': 'amount'}).groupby(by=['problem_id', 'success']).count().reset_index()[['problem_id',
                                                                                                          'success',
                                                                                                          'amount']]
    problem_id_map = {i: j for i, j in
                      zip(pd.unique(df['problem_id']), range(0, len(pd.unique(df['problem_id']))))}
    df['id_new'] = df['problem_id'].map(problem_id_map)
    amount_problem = pd.unique(df.id_new).shape[0]
    for i in range(0, math.ceil(amount_problem / 50)):
        # fig = plt.subplots(figsize=(25, 10))
        # ax.bar(x - width/2, g1, width, label='g1')
        sns.barplot(data=df.loc[(df.id_new >= i * 50) & (df.id_new < (i + 1) * 50 - 1)], x='id_new',
                    y='amount', hue='success')
        plt.legend(title=None)
        plt.xticks(rotation=90)
        plt.title('Количество удачных/неудачных попыток')
        plt.xlabel('id задания')
        plt.ylabel('Количество попыток')
        plt.show()


def course_activity_period(df):
    df['date'] = df.time_event.apply(lambda x: x.date())
    df_temp = df.groupby(by=['date']).count().reset_index()
    plt.plot(df_temp['date'], df_temp['id'], '.-b', mfc='r', ms=7, linewidth=1)
    # plt.xticks(df_temp['date'], rotation=90)
    plt.xticks(rotation=90)
    plt.title('Активность на курсе')
    plt.xlabel('Дата')
    plt.ylabel('Количество событий')
    plt.grid()
    plt.show()


def course_activity_day(df):
    df['hour'] = df.time_event.apply(lambda x: x.time().hour)
    df_temp = df[['user_id', 'hour', 'id']].groupby(by=['user_id', 'hour']).count().groupby(
        by=['hour']).mean().reset_index()
    plt.plot(df_temp['hour'], df_temp['id'], '.-b', mfc='r', ms=10, linewidth=1)
    # plt.xlabel.set_major_locator(ticker.AutoLocator())
    plt.xticks(np.arange(min(df_temp['hour']), max(df_temp['hour']) + 1, 1), rotation=90)
    plt.title('Средняя активность на курсе в течении дня')
    # xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.xlabel('Время')
    plt.ylabel('Количество событий')
    plt.grid()
    plt.show()


def course_complete_avg(df):
    # df_temp = pd.DataFrame(columns=['user_id', 'time'])
    df = df.groupby('user_id')['time_event'].max() - df.groupby('user_id')['time_event'].min()
    print('Среднее время участия студента на курсе: ', df.mean())


def problem_info(course_id):
    query = models.ProblemInteractionEvent.select().where(models.ProblemInteractionEvent.course_id == course_id)
    df = pd.DataFrame(query.dicts())
    percent_compl_tasks(df)
    amount_success_tasks(df)
    course_activity_period(df)
    course_activity_day(df)
    course_complete_avg(df)


def materials_info(course_id):
    query_book = models.BookEvent.select().where(models.BookEvent.course_id == course_id)
    query_video = models.VideoInteractionEvent.select().where((models.VideoInteractionEvent.course_id == course_id) &
                                                              (models.VideoInteractionEvent.type_event == 'play_video'))
    df_book = pd.DataFrame(query_book.dicts())
    df_video = pd.DataFrame(query_video.dicts())
    plt.bar(['Документы', 'Видео'], [df_book.shape[0], df_video.shape[0]])
    plt.title('Количество обращений к материалам курса')
    plt.ylabel('Количество обращений')
    plt.show()
