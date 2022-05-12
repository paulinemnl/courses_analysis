import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import analysis

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn import preprocessing


pd.set_option('display.max_columns', 20)


def info_interactions(df_all):
    df_temp = df_all[['seasons', 'cluster']].copy()
    df_temp.columns = df_temp[['seasons', 'cluster']].columns.droplevel()
    df_temp.rename(columns={'': 'cluster'}, inplace=True)
    df_mean_T = df_temp.groupby('cluster').mean().T
    y_max = df_mean_T.max().max()
    for i in df_mean_T.columns:
        plt.figure(figsize=(df_mean_T.shape[0] / 1.5, 9))
        plt.bar(df_mean_T[[i]].index, df_mean_T[i])
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.xlabel(str(i) + ' кластер', fontsize=16)
        plt.xticks(rotation=90)
        plt.ylim(0, y_max + 10)
        plt.ylabel('Количество взаимодействий', fontsize=16)
        plt.show()


def info_problem(df_all):
    df_temp = df_all[['problem_id', 'cluster']].copy()
    df_temp = df_temp.replace(0, np.NaN)
    df_temp.columns = df_temp[['problem_id', 'cluster']].columns.droplevel()
    df_temp.rename(columns={'': 'cluster'}, inplace=True)
    df_mean_T = df_temp.groupby('cluster').mean().T
    df_mean_T.index = df_mean_T.index.astype(int)
    y_max = df_mean_T.max().max()
    for i in df_mean_T.columns:
        ax = plt.figure(figsize=(20, 10))
        for j in range(0, math.ceil(df_mean_T.shape[0] / 50)):
            ax = plt.figure(figsize=(25, 10))
            sns.barplot(data=df_mean_T.loc[
                ((df_mean_T.index >= (j * 50)) & (df_mean_T.index < (j + 1) * 50)), i].reset_index(),
                        x='index', y=i, color='blue')
            plt.tick_params(axis='both', which='major', labelsize=16)
            plt.xlabel(str(i) + ' кластер', fontsize=16)
            plt.xticks(rotation=90)
            plt.ylim(0, y_max + 1)
            plt.title('Среднее количество попыток', fontsize=25)
            plt.ylabel('Количество попыток', fontsize=16)
            plt.show()


def info_materials(df_all):
    df_temp = df_all[['others', 'cluster']].copy()
    df_temp.columns = df_all[['others', 'cluster']].columns.droplevel()
    df_temp.rename(columns={'': 'cluster'}, inplace=True)
    df_mean = df_temp.groupby('cluster').mean()
    df_mean.columns = ['video', 'book', 'percent']
    df_mean = df_mean.iloc[:, :-1].stack()
    df_mean.name = 'values'
    df_mean = df_mean.reset_index()
    df_mean.columns = ['cluster', 'materials', 'values']
    sns.barplot(data=df_mean, x='materials', y='values', hue='cluster')
    plt.title('Среднее количество обращений к материалам')
    plt.xlabel('Вид материала')
    plt.ylabel('Количество обращений')
    plt.show()


def info_percent(df_all):
    df_temp = df_all[['others', 'cluster']].copy()
    df_temp.columns = df_all[['others', 'cluster']].columns.droplevel()
    df_temp.rename(columns={'': 'cluster'}, inplace=True)
    # df2['cluster'] = fcluster(link, 3, criterion='maxclust')
    df_mean = df_temp.groupby('cluster').mean()
    df_mean.columns = ['video', 'book', 'percent']
    plt.bar((df_mean.index.values).astype(str), df_mean['percent'])
    plt.title('Процент выполнения заданий')
    plt.xlabel('Кластер')
    plt.ylabel('%')
    plt.show()


def clustering(df_problem, df_book, df_video):
    df_problem = df_problem.assign(seasons=df_problem['time_event'].dt.strftime('%m-%y'))
    df_problem = df_problem.assign(action=1)
    df_clast_seasons = pd.pivot_table(df_problem, index='user_id', columns='seasons', values='action', aggfunc=np.sum,
                                      fill_value=0)
    df_clast_seasons = df_clast_seasons.reindex(
        columns=pd.Series(sorted(pd.to_datetime(df_clast_seasons.columns.to_list(), format="%m-%y"))).dt.strftime(
            "%m-%y"))
    df_clast_seasons.columns.name = None
    df_clast_seasons.columns = pd.MultiIndex.from_product([['seasons'], df_clast_seasons.columns])
    problem_id_map = {i: j for i, j in
                      zip(pd.unique(df_problem['problem_id']), range(0, len(pd.unique(df_problem['problem_id']))))}
    df_problem = df_problem.assign(problem_id_num=df_problem['problem_id'].map(problem_id_map))
    df_clast_problem = df_problem.pivot_table(index="user_id", columns="problem_id_num", values='attempts',
                                              fill_value=0, aggfunc=np.max)
    df_clast_problem.columns.name = None
    df_clast_problem.columns = pd.MultiIndex.from_product([['problem_id'], df_clast_problem.columns.astype(str)])
    df_clast_video_book = df_video.groupby(by='user_id').count()[['video_id']].merge(
        df_book.groupby(by='user_id').count()[['chapter']], on='user_id', how='outer')
    df_user_percent = pd.DataFrame(columns=['user_id', 'percent'])
    amount_of_problem = pd.unique(df_problem['problem_id']).shape[0]
    for i in pd.unique(df_problem['user_id']):
        df_user_percent.loc[len(df_user_percent)] = [i, df_problem[
            (df_problem.user_id == i) & (df_problem.success == 'correct')].shape[
            0] / amount_of_problem * 100]
    df_clast_others = df_clast_video_book.merge(df_user_percent, on='user_id', how='outer')
    df_clast_others = df_clast_others.set_index('user_id').fillna(0)
    df_clast_others.columns = pd.MultiIndex.from_product([['others'], df_clast_others.columns])
    df_all = df_clast_seasons.merge(df_clast_problem, on='user_id', how='outer').merge(df_clast_others, on='user_id',
                                                                                       how='outer')
    df_all = df_all.loc[df_all.others.percent != 0]
    X = df_all.copy()
    X.columns = X.columns.droplevel()
    norm = preprocessing.StandardScaler()
    norm.fit(X)
    X_norm = norm.transform(X)
    X_norm = pd.DataFrame(X_norm, index=X.index, columns=X.columns)
    link = linkage(X_norm.to_numpy(), 'ward', 'euclidean')
    dendrogram(link, labels=np.array(X_norm.index), truncate_mode='lastp', color_threshold=5, orientation="right",
               leaf_rotation=0.)
    plt.title('Дендрограмма')
    plt.ylabel('Кластеры')
    plt.xlabel('Расстояние')
    plt.show()
    dist = link[:, 2]
    dist_rev = dist[::-1]
    idxs = range(1, len(dist) + 1)
    plt.plot(idxs[:30], dist_rev[:30], marker='o')
    plt.title('Метод "локтя"')
    plt.xlabel('Количество кластеров')
    plt.ylabel('Расстояние')
    plt.show()
    n_cluster = int(input('Введите количество кластеров: '))
    df_all['cluster'] = fcluster(link, n_cluster, criterion='maxclust')
    print(df_all.groupby('cluster').size())
    info_interactions(df_all)
    info_problem(df_all)
    info_materials(df_all)
    info_percent(df_all)
