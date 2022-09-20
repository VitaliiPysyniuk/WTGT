import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
import os
import shutil


def build_result_chart(vote_results):
    restaurant_names = []
    votes_number = []

    for item in vote_results:
        restaurant_names.append(item['menu__restaurant__name'])
        votes_number.append(item['votes'])

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.barplot(x=restaurant_names, y=votes_number, ax=ax, palette='plasma', alpha=0.8)
    ax.set_title(f'Vote results for {date.today()}', backgroundcolor='#565656', fontsize=20, weight='bold',
                 color='white', style='italic', loc='center', pad=30)
    ax.tick_params(labelsize=16, length=0)
    plt.box(False)

    ax.yaxis.grid(linewidth=0.5, color='grey', linestyle='-.')
    ax.set_axisbelow(True)
    ax.set_xlabel('Restaurants', weight='bold', size=15)
    ax.set_ylabel('Votes number', weight='bold', size=15)

    plt.yticks(color='#565656', ticks=range(0, max(votes_number) + 1, 1))
    plt.xticks(color='#565656')

    directory = 'charts'
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)

    filepath = f'{directory}/vote-results-{date.today()}'
    plt.savefig(filepath)

    return filepath


def parse_results(vote_results):
    data = list()
    for vote_result in vote_results:
        result_item = dict()
        result_item['restaurant'] = {
            'id': vote_result['menu__restaurant_id'],
            'name': vote_result['menu__restaurant__name']
        }
        result_item['votes_number'] = vote_result['votes']
        data.append(result_item)

    return data
