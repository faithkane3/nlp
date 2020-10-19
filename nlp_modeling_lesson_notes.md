# NLP Modeling

How do we quantify a document?

- [Setup](#setup)
- [Data Representation](#data-representation)
    - [Bag of Words](#bag-of-words)
    - [TF-IDF](#tf-idf)
    - [Bag Of Ngrams](#bag-of-ngrams)
- [Modeling](#modeling)
    - [Modeling Results](#modeling-results)
- [Next Steps](#next-steps)

## Setup

```python
from pprint import pprint
import pandas as pd
import nltk
import re

def clean(text: str) -> list:
    'A simple function to cleanup text data'
    wnl = nltk.stem.WordNetLemmatizer()
    stopwords = set(nltk.corpus.stopwords.words('english'))
    text = (text.encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
    words = re.sub(r'[^\w\s]', '', text).split() # tokenization
    return [wnl.lemmatize(word) for word in words if word not in stopwords]
```

## Data Representation

Simple data for demonstration.

```python
data = [
    'Python is pretty cool',
    'Python is a nice programming language with nice syntax',
    'I think SQL is cool too',
]
```

### Bag of Words

```python
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
bag_of_words = cv.fit_transform(data)
```

```python
bag_of_words.todense()
```

```python
cv.get_feature_names()
```

Here `bag_of_words` is a **sparse matrix**. Usually you should keep it as such,
but for demonstration we'll view the data within.

```python
pprint(data)
pd.DataFrame(bag_of_words.todense(), columns=cv.get_feature_names())
```

### TF-IDF

- a measure that helps identify how important a word is in a document
- combination of how often a word appears in a document (**tf**) and how unqiue the word
  is among documents (**idf**)
- used by search engines
- naturally helps filter out stopwords
- tf is for a single document, idf is for a corpus

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()
bag_of_words = tfidf.fit_transform(data)

pprint(data)
pd.DataFrame(bag_of_words.todense(), columns=tfidf.get_feature_names())
```

```python
tfidf.idf_
```

```python
tfidf.get_feature_names()
```

```python
pd.Series(dict(zip(tfidf.get_feature_names(), tfidf.idf_))).sort_values()
```

### Bag Of Ngrams

For either `CountVectorizer` or `TfidfVectorizer`, you can set the `ngram_range`
parameter.

```python
cv = CountVectorizer(ngram_range=(2, 2))
bag_of_words = cv.fit_transform(data)
```

```python
pprint(data)
pd.DataFrame(bag_of_words.todense(), columns=cv.get_feature_names())
```

## Modeling

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('spam_clean.csv')
```

```python
df.head()
```

```python
cv = CountVectorizer()
X = cv.fit_transform(df.text.apply(clean).apply(' '.join))
y = df.label
```

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=12)
```

```python
pd.DataFrame(X_train[:5, :].todense(), columns=cv.get_feature_names())
```

```python
tree = DecisionTreeClassifier(max_depth=5)
tree.fit(X_train, y_train)

tree.score(X_train, y_train)
```

```python
tree.predict(X_train)
```

```python
tree.score(X_test, y_test)
```

### Modeling Results

A super-useful feature of decision trees and linear models is that they do some
built-in feature selection through the coefficeints or feature importances:

```python
cv.get_feature_names()
```

```python
tree.feature_importances_
```

```python
pd.Series(dict(zip(cv.get_feature_names(), tree.feature_importances_))).sort_values().tail(12)
```

## Next Steps

- Try other model types

    [Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)
    ([`sklearn`
    docs](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html))
    is a very popular classifier for NLP tasks.

- Look at other metrics, is accuracy the best choice here?

- Try ngrams instead of single words

- Try a combination of ngrams and words (`ngram_range=(1, 2)` for words and
  bigrams)

- Try using tf-idf instead of bag of words

- Combine the top `n` performing words with the other features that you have
  engineered (the `CountVectorizer` and `TfidfVectorizer` have a `vocabulary`
  argument you can use to restrict the words used)

    ```python
    best_words = (
        # or, e.g. lm.coef_
        pd.Series(dict(zip(cv.get_feature_names(), tree.feature_importances_)))
        .sort_values()
        .tail(5)
        .index
    )

    cv = CountVectorizer(vocabulary=best_words)
    X = cv.fit_transform(df.text.apply(clean).apply(' '.join))

    # for demonstration
    pd.DataFrame(X.todense(), columns=cv.get_feature_names())
    ```
