import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math


def users_percent_task(df):
    df_user_percent = pd.DataFrame(columns=['user_id', 'percent_suc_attemp', 'percent_comp_task'])
    amount_of_problem = pd.unique(df['problem_id']).shape[0]
    for i in pd.unique(df['user_id']):
        df_user_percent.loc[len(df_user_percent)] = [i, df[
            (df.user_id == i) & (df.success == 'correct')].shape[
            0] / df[(df.user_id == i)].shape[0] * 100, df[(df.user_id == i) & (df.success == 'correct')].shape[
                                                         0] / amount_of_problem * 100]
    return df_user_percent


def users_unappropr(df):
    df_user_percent = users_percent_task(df)
    users_cheated = df_user_percent.loc[
        ((df_user_percent.percent_suc_attemp == 100) & (df_user_percent.percent_comp_task >= 75)), 'user_id']
    users_zero_prog = df_user_percent.loc[(df_user_percent.percent_comp_task == 0), 'user_id']
    if not users_cheated.empty:
        print('Студенты, подозреваемые в списывании: ')
        print(df_user_percent.loc[df_user_percent['user_id'].isin(users_cheated)])
    return users_cheated, users_zero_prog


def percent_compl_tasks(df):
    df_user_percent = users_percent_task(df)
    df_wo = df_user_percent[(df_user_percent.percent_comp_task != 0)]
    plt.figure(figsize=(6, 4))
    plt.hist(df_wo['percent_comp_task'], range=(0, 100))
    plt.locator_params(axis='y', integer=True)
    plt.title('Процент выполненных заданий')
    plt.ylabel('Количество учащихся')
    plt.xlabel('%')
    plt.show()
    return df_user_percent


def amount_success_tasks(df):
    df_succ = df.rename(columns={'id': 'amount'}).groupby(by=['problem_id', 'success']).count().reset_index()[[
        'problem_id', 'success', 'amount']]
    problem_id_map = {i: j for i, j in
                      zip(pd.unique(df_succ['problem_id']), range(0, len(pd.unique(df_succ['problem_id']))))}
    df_succ['id_new'] = df_succ['problem_id'].map(problem_id_map)
    amount_problem = pd.unique(df_succ.id_new).shape[0]
    df_pivot = pd.pivot_table(df_succ, index=['id_new', 'problem_id'], columns='success', values='amount',
                              aggfunc=np.sum).reset_index()
    df_task_susp = df_pivot[(df_pivot.correct == 0) & ((df_pivot.incorrect > 0))]
    if not df_task_susp.empty:
        print('Задания, возможно составленные с ошибкой:')
        print(df_task_susp)
    for i in range(0, math.ceil(amount_problem / 30)):
        sns.barplot(data=df_succ.loc[(df_succ.id_new >= i * 30) & (df_succ.id_new < (i + 1) * 30 - 1)], x='id_new',
                    y='amount', hue='success')
        plt.legend(title=None)
        plt.xticks(rotation=90)
        plt.title('Количество удачных/неудачных попыток')
        plt.xlabel('id задания')
        plt.ylabel('Количество попыток')
        plt.show()


def course_activity_period(df):
    df = df.assign(date=lambda x: x.time_event.dt.date)
    df_temp = df.groupby(by=['date']).count().reset_index()
    plt.figure(figsize=(13, 10))
    plt.plot(df_temp['date'], df_temp['id'], '.-b', mfc='r', ms=7, linewidth=1)
    plt.xticks(rotation=90, fontsize=12)
    plt.title('Активность на курсе', fontsize=16)
    plt.xlabel('Дата', fontsize=16)
    plt.ylabel('Количество событий', fontsize=16)
    plt.grid()
    plt.show()


def course_activity_day(df):
    df = df.assign(hour=lambda x: x.time_event.dt.hour)
    df_temp = df[['user_id', 'hour', 'id']].groupby(by=['user_id', 'hour']).count().groupby(by=['hour']).mean().reset_index()
    plt.plot(df_temp['hour'], df_temp['id'], '.-b', mfc='r', ms=10, linewidth=1)
    plt.xticks(np.arange(min(df_temp['hour']), max(df_temp['hour']) + 1, 1), rotation=90)
    plt.title('Средняя активность на курсе в течении дня')
    plt.xlabel('Время')
    plt.ylabel('Количество событий')
    plt.grid()
    plt.show()


def course_complete_avg(df):
    df_time = df.groupby('user_id')['time_event'].max() - df.groupby('user_id')['time_event'].min()
    print('Среднее время участия студента на курсе: ', str(df_time.mean()).split(".")[0])


def course_info(df_problem, df_book, df_video):
    users_cheated, users_zero_prog = users_unappropr(df_problem)
    df_problem = df_problem.loc[~df_problem['user_id'].isin(pd.concat([users_cheated, users_zero_prog]))]
    df_book = df_book.loc[~df_book['user_id'].isin(pd.concat([users_cheated, users_zero_prog]))]
    df_video = df_video.loc[~df_video['user_id'].isin(pd.concat([users_cheated, users_zero_prog]))]
    percent_compl_tasks(df_problem)
    amount_success_tasks(df_problem)
    course_activity_period(df_problem)
    course_activity_day(df_problem)
    course_complete_avg(df_problem)
    plt.bar(['Документы', 'Видео'], [df_book.shape[0], df_video.shape[0]])
    plt.title('Количество обращений к материалам курса')
    plt.ylabel('Количество обращений')
    plt.show()


