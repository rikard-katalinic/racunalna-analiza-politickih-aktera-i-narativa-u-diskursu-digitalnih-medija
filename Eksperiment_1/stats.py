import pandas as pd

def isNotFloat(num):
    try:
        float(num)
        return False
    except ValueError:
        return True

izbori = pd.read_excel('clanci/articles_index.xlsx')
df = pd.DataFrame(izbori)
articles = list(df['Content'])

sentences_sum = 0
words_sum = 0
unique_words = set()

for article in articles:
    if isNotFloat(article):
        sentences = article.split('.')
        sentences_sum += len(sentences)

        words = article.split()
        words_sum += len(words)
        unique_words.update(words)

print("Broj članaka:", len(articles))
print("Broj riječi:", words_sum)
print("Broj jedinstvenih (unique) riječi:", len(unique_words))
print("Broj rečenica:", sentences_sum)