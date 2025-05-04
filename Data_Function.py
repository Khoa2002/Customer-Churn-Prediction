import pandas as pd
import matplotlib.pyplot as plt

def stacked_plot(data, features, target, ax, colors=None): 
    df = (
        data.groupby([features, target])
            .size() * 100
        / data.groupby(features)[target].count()
    ).reset_index()\
     .pivot(columns=target, index=features, values=0)

    df.plot(kind='bar', stacked=True, ax=ax, color=colors)
    plt.grid(axis = 'y')
    ax.set_axisbelow(True)
    ax.xaxis.set_tick_params(rotation=0)
    ax.set_title(f'% Churn {features}')
    ax.set_xlabel(features)

def stacked_table(data, feature, target):
    df = (
        data.groupby([feature, target])
            .size() * 100
        / data.groupby(feature)[target].count()
    ).reset_index()\
     .pivot(columns=target, index=feature, values=0)

    df.columns = [f'Churn_{col} (%)' for col in df.columns]
    return df.round(2)

def get_color_palettes():
    churn_1 = ['#ff3838']
    churn_2 = ['#F21616', '#777777']  #'#ff3838'
    churn_5 = ['#CB0000', '#F21616', '#F24747', '#F26868', '#FC9F9F']
    churn_10 = ['#f00000','#ff2424','#ff3838','#ff554f','#fb7571','#cccccc','#b6b6b6','#9e9e9e','#888888','#777777']    
    return churn_1, churn_2, churn_5, churn_10