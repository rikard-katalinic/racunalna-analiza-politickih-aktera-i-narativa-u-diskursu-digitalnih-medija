from transformers import pipeline
import torch
import stanza
from transformers import AutoTokenizer, AutoModelForTokenClassification
import pandas as pd

def perform_ner(texts):
    extracted_data = []
    all_sentences = []
    metadata = []

    stanza.download("hr")
    nlp = stanza.Pipeline("hr", processors="tokenize")
    separator = "\n\n<<<DOC_BOUNDARY>>>\n\n"
    combined_text = separator.join(text for _, text in texts)
    
    doc = nlp(combined_text)
    current_month_index = 0
    months = [month for month, _ in texts]

    for sentence in doc.sentences:
        sent_text = sentence.text
        if "<<<DOC_BOUNDARY>>>" in sent_text:
            current_month_index += 1
            continue
        all_sentences.append(sent_text)
        metadata.append(months[current_month_index])
    
    ner_pipeline = pipeline(
        "ner",
        model = AutoModelForTokenClassification.from_pretrained("classla/bcms-bertic-ner"),
        tokenizer = AutoTokenizer.from_pretrained("classla/bcms-bertic-ner", use_fast=True),
        device = 0 if torch.cuda.is_available() else -1,
        aggregation_strategy="simple"
    )
    with torch.inference_mode():
        results = ner_pipeline(list(all_sentences), batch_size=64)

    for month, sentence, entities in zip(metadata, all_sentences, results):
        extracted_data.extend(
            {
                "month": month,
                "entity": ent["word"],
                "sentence": sentence
            }
            for ent in entities
            if ent["entity_group"] in {"PER", "ORG"}
        )

    entity_df = pd.DataFrame(extracted_data)
    entity_df.to_csv('/entities.csv', index=False, sep='|')
    print("\nEntiteti su izlučeni!")


def add_person(df):
    stanza.download("hr")

    ner_pipeline = pipeline(
        "ner",
        model=AutoModelForTokenClassification.from_pretrained("classla/bcms-bertic-ner"),
        tokenizer=AutoTokenizer.from_pretrained("classla/bcms-bertic-ner", use_fast=True),
        device=0 if torch.cuda.is_available() else -1,
        aggregation_strategy="simple"
    )
    entities = df['entity'].tolist()

    # Batch processing
    results = ner_pipeline(entities, batch_size=32)

    mapping = {}
    for entity, res in zip(entities, results):
        if not res:
            mapping[entity] = 0
        else:
            mapping[entity] = int(any(r.get('entity_group') == 'PER' for r in res))

    df['person'] = df['entity'].map(mapping)
    df.to_csv("dataset_person.csv", sep=";", index=False)