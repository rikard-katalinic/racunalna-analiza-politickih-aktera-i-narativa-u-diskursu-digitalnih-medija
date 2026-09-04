from matplotlib import pyplot as plt

"""
def visualize_entity_sentiments(df, politicians=True, portal=False):
    import numpy as np
    sentiment_order = ["Positive", "Negative", "Neutral"]
    if not portal:
        df = (
            df.groupby(["month", "entity", "sentiment"])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        df = df.reindex(columns=["month", "entity"] + sentiment_order, fill_value=0)

    entities = None
    if portal:
        entities = df["entity"].unique()
        portals = df["portal"].unique()
        x = np.arange(len(entities))
    else:
        months = sorted(df["month"].unique())
        x = np.arange(len(months))

    bar_width = 0.25
    offsets = [-bar_width, 0, bar_width]

    colors = {
        "Positive": "green",
        "Negative": "orange",
        "Neutral": "lightblue"
    }
    _, ax = plt.subplots(figsize=(12, 6))

    group_key = "portal" if portal else "month"
    groups = portals if portal else months

    for j, entity in enumerate(entities):

        entity_data = df[df["entity"] == entity]

        entity_data = (
            entity_data.assign(total=lambda d: d[sentiment_order].sum(axis=1))
            .sort_values("total", ascending=False)
            .drop(columns="total")
            .reset_index(drop=True)
        )

        for i, (_, row) in enumerate(entity_data.iterrows()):
            pos = x[j] + offsets[i]
            bottom = 0
            for sentiment in sentiment_order:
                ax.bar(
                    pos, row[sentiment],
                    bar_width,
                    bottom = bottom,
                    color = colors[sentiment],
                    edgecolor = "black"
                )
                bottom += row[sentiment]

            ax.text(
                pos,
                bottom + 70 if portal else bottom + 40,
                row["portal"] if portal else row["entity"],
                ha="center",
                fontsize = 9,
                rotation = 90
            )
    ax.set_xticks(x)
"""

# for person/organization division
def visualize_entity_sentiments(df):
    import numpy as np
    import matplotlib.pyplot as plt

    sentiment_order = ["Positive", "Negative", "Neutral"]

    df_grouped = (
        df.groupby(["month", "person"])[sentiment_order]
        .sum()
        .reset_index()
    )

    months = sorted(df_grouped["month"].unique())
    x = np.arange(len(months))
    bar_width = 0.35
    offsets = [-bar_width/2, bar_width/2]  

    colors = {
        "Positive": "green",
        "Negative": "orange",
        "Neutral": "lightblue"
    }

    labels_map = {1: "P", 0: "O"}
    month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    _, ax = plt.subplots(figsize=(12, 6))

    for i, month in enumerate(months):
        month_data = df_grouped[df_grouped["month"] == month]

        for j, person_type in enumerate([1, 0]):  
            row = month_data[month_data["person"] == person_type]

            if row.empty:
                values = {s: 0 for s in sentiment_order}
            else:
                values = row.iloc[0]

            pos = x[i] + offsets[j]
            bottom = 0
            for sentiment in sentiment_order:
                val = values[sentiment] if sentiment in values else 0
                ax.bar(
                    pos, val,
                    bar_width,
                    bottom = bottom,
                    color = colors[sentiment],
                    edgecolor = "black",
                    alpha = 1.0 if person_type == 1 else 0.5
                )
                bottom += val

            ax.text(
                pos,
                bottom + 10,
                labels_map[person_type],
                ha = "center",
                fontsize = 18
            )

    ax.set_xticks(x)
    ax.set_xticklabels([month_labels[m-1] for m in months])

    ax.set_xlabel("Month", fontsize=20, labelpad=15)
    ax.set_ylabel("Number of sentences", fontsize=20, labelpad=15)
    #ax.set_title("Sentiments persons and organizations per month", fontsize=14, pad=15)
    ax.tick_params(axis='both', labelsize=18)

    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor="green", label="Positive"),
        Patch(facecolor="orange", label="Negative"),
        Patch(facecolor="lightblue", label="Neutral")
    ], fontsize=18)

    plt.tight_layout()
    plt.show()

"""
# politicians / organizations
def visualize_entity_sentiments(df, politicians=True, portal=False):
    import numpy as np
    sentiment_order = ["Positive", "Negative", "Neutral"]
    if not portal:
        df = (
            df.groupby(["month", "entity", "sentiment"])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        df = df.reindex(columns=["month", "entity"] + sentiment_order, fill_value=0)

    entities = None
    if portal:
        entities = df["entity"].unique()
        portals = df["portal"].unique()
        x = np.arange(len(entities))
    else:
        months = sorted(df["month"].unique())
        x = np.arange(len(months))

    bar_width = 0.25
    offsets = [-bar_width, 0, bar_width]

    colors = {
        "Positive": "green",
        "Negative": "orange",
        "Neutral": "lightblue"
    }
    _, ax = plt.subplots(figsize=(12, 6))

    group_key = "portal" if portal else "month"
    groups = portals if portal else months

    for i, group in enumerate(groups):
        group_data = df[df[group_key] == group]

        group_data = (
            group_data.assign(total=lambda d: d[sentiment_order].sum(axis=1))
            .sort_values("total", ascending=False)
            .drop(columns="total")
            .reset_index(drop=True)
        )

        for j, (_, row) in enumerate(group_data.iterrows()):
            # choose position logic depending on grouping
            pos = x[j] + offsets[i] if portal else x[i] + offsets[j % len(offsets)]

            bottom = 0
            for sentiment in sentiment_order:
                ax.bar(
                    pos, row[sentiment],
                    bar_width,
                    bottom = bottom,
                    color = colors[sentiment],
                    edgecolor = "black"
                )
                bottom += row[sentiment]

            ax.text(
                pos,
                bottom + 70 if portal else bottom + 40,
                row["portal"] if portal else row["entity"],
                ha = "center",
                fontsize = 9,
                rotation = 90
            )
    ax.set_xticks(x)

    if portal:
        ax.set_xticklabels(entities, rotation=45, ha="right")
    else:
        ax.set_xticklabels(months)

    ax.set_xlabel("Entities" if portal else "Month", fontsize=12)
    ax.set_ylabel("Number of sentences", fontsize=12)
    #type = 'politicians' if politicians else 'parties'
    #ax.set_title("Sentiments for top 3 {} per month".format(type), fontsize=14, pad=15)

    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor="green", label="Positive"),
        Patch(facecolor="orange", label="Negative"),
        Patch(facecolor="lightblue", label="Neutral")
    ])

    plt.tight_layout()
    plt.show()
"""


def plot_scatter(df, per_month):
    df['total'] = df['Positive'] + df['Negative'] + df['Neutral']
    df['score'] = (df['Positive'] - df['Negative']) / df['total']
    #df = df[df['total'] >= 20]

    plt.figure(figsize=(10, 7))
    if per_month:
        entities = df['entity'].unique()
        colors = plt.cm.tab10.colors 

        for i, entity in enumerate(entities):
            subset = df[df['entity'] == entity].sort_values('month')
            marker = 'o' if subset['person'].iloc[0] == 1 else 's'

            plt.scatter(
                subset['total'],
                subset['score'],
                color=colors[i % 10],
                marker=marker,
                alpha=0.6
            )

        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Politician',
                markerfacecolor='gray', markersize=8),
            Line2D([0], [0], marker='s', color='w', label='Organization',
                markerfacecolor='gray', markersize=8)
        ]
        plt.legend(handles=legend_elements)
    else:
        df_person = df[df['person'] == 1]
        df_org = df[df['person'] == 0]

        print("Total:", len(df))
        print("Persons:", len(df_person))
        print("Organizations:", len(df_org))

        plt.scatter(df_person['total'], df_person['score'], label='Politician', alpha=0.5)
        plt.scatter(df_org['total'], df_org['score'], label='Organization', alpha=0.5)
        plt.legend()

    """
    top10 = df.nlargest(10, 'total')
    for _, row in top10.iterrows():
        plt.text(row['total'] + 0.5, row['score'], row['entity'], fontsize=8)
    """

    plt.xlabel('Total mentions', fontsize=10)
    plt.ylabel('Normalized sentiment balance', fontsize=12)
    plt.title('Entity sentiment scatter per month (log scale)', fontsize=14, pad=15)

    plt.axhline(y=0, color='black', linestyle='-')
    plt.xscale('log')
    plt.ylim(-1, 1)
    plt.tight_layout()
    plt.show()


def plot_bubble_timeline(df):
    df['total'] = df['Positive'] + df['Negative'] + df['Neutral']
    df['score'] = (df['Positive'] - df['Negative']) / df['total']

    entities = df['entity'].unique()
    entity_to_y = {e: i for i, e in enumerate(entities)}
    df['y'] = df['entity'].map(entity_to_y)

    month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    df['month_label'] = df['month'].apply(lambda x: month_labels[x-1])

    plt.figure(figsize=(15, 7), constrained_layout=True)
    scatter = plt.scatter(
        df['month'], df['y'],
        s=df['total'],
        c=df['score'],
        cmap='viridis',
        alpha=0.8
    )

    plt.xticks(range(1, 13), month_labels, fontsize=12)
    plt.yticks(list(entity_to_y.values()), list(entity_to_y.keys()), fontsize=12)
    plt.xlabel('Month', fontsize=14, labelpad=15)
    plt.ylabel('Entity', fontsize=14)

    cbar = plt.colorbar(scatter, pad=0.02, fraction=0.1)
    cbar.set_label('Normalized sentiment balance', fontsize=13, labelpad=15)
    cbar.ax.tick_params(labelsize=11)

    plt.title(
        'Bubble timeline of entity visibility and sentiment dynamics across months',
        fontsize=16, pad=15
    )
    plt.grid(axis='x', alpha=0.2)
    plt.show()


def plot_bump_chart(df):
    df['total'] = df['Positive'] + df['Negative'] + df['Neutral']

    
    df['rank'] = (
        df.groupby('month')['total']
          .rank(method='first', ascending=False)
    )

    pivot = df.pivot(index='entity', columns='month', values='rank')

    pivot['avg_rank'] = pivot.mean(axis=1)
    pivot = pivot.sort_values('avg_rank').drop(columns='avg_rank')

    plt.figure(figsize=(13, 8))
    colors = plt.cm.tab10.colors 
    month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for i, entity in enumerate(pivot.index):
        y = pivot.loc[entity]

        plt.plot(
            pivot.columns, y,
            marker='o',
            label=entity,
            color=colors[i % len(colors)]
        )

        plt.text(
            pivot.columns.max() + 0.1,
            y.iloc[-1],
            entity,
            fontsize=17,
            va='center'
        )

    plt.gca().invert_yaxis()  # rank 1 on top
    plt.xticks(range(1, 13), month_labels, fontsize=18)
    plt.yticks(range(1, 11), fontsize=18)

    plt.xlabel('Month', fontsize=20, labelpad=15)
    plt.ylabel('Rank (1 = highest visibility)', fontsize=20)
    #plt.title('Bump chart of monthly rank changes', fontsize=16, pad=15)

    plt.grid(axis='y', alpha=0.2)
    plt.legend().remove()
    plt.tight_layout()
    plt.show()