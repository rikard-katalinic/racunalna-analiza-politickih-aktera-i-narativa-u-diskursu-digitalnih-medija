#from transformers import pipeline
#import torch
import pandas as pd

def sentiment_analysis(df, entity_dict, by_month):
    sentiment = pipeline(
        "sentiment-analysis",
        model="classla/bcms-bertic-parlasent-bcs-ter",
        tokenizer="classla/bcms-bertic-parlasent-bcs-ter",
        device = 0 if torch.cuda.is_available() else -1
    )

    df_filtered = None
    if by_month:
        mask = [
            row.entity in entity_dict.get(row.month, set())
            for row in df.itertuples()
        ]
        df_filtered = df[mask].copy()
    else:
        df_filtered = df[df["entity"].isin(entity_dict)].copy()

    df_filtered["sentence"] = [
        row.sentence.replace(row.entity, "[TARGET]")
        for row in df_filtered.itertuples()
    ]

    results = sentiment(
        df_filtered["sentence"].tolist(),
        batch_size=32,
        truncation=True
    )

    df_filtered["sentiment"] = [r["label"] for r in results]
    df_filtered[["month", "entity", "sentiment", "portal"]].to_csv(
        "test.csv", index=False, sep="|"
    )
    print("\nSentiment analysis completed!")


def get_sentiment_stats(sentiment_df, group_by):
    if group_by == "total":
        sentiment_summary = pd.pivot_table(
            sentiment_df,
            index='entity',
            columns='sentiment',
            aggfunc='size',
            fill_value=0
        ).reset_index()
        sentiment_summary = sentiment_summary[['entity', 'Positive', 'Negative', 'Neutral']]
        sentiment_summary.to_csv('sentimenti/sentiments_total.csv', index=False, sep='|')
    else:
        criterion = "month" if group_by == "month" else "portal"
        sentiment_summary = (
            sentiment_df
                .groupby([criterion, "entity", "sentiment"])
                .size()
                .unstack(fill_value=0)
                .reset_index()
        )
        sentiment_summary.to_csv(f'sentimenti/sentiments_per_{criterion}.csv', index=False, sep='|')