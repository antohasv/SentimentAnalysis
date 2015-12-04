В качестве языка программирования использовался Python с пакетным менеджером Anacondas
Для анализа и обучения использовались библиотеки: scikit learn, pandas, numpy, nltk, word2vec
В качестве среды разработки использовался ipython notebook

Данные для анализа подготовлены в excel Sentiment_Analysis_Dataset.csv

Обучение с учителем:
BagOfWord.ipynb
Word2Vec.ipynb

Алгоритмы машинного обучения:
RandomForest
GaussianNB (наивный байесовский классификатор)

Для извлечения Twiteet используется скрипт load_tweets/load_tweet.py
Для получения твитов нужно пользователю авторизоваться(можно неявно авторизовать пользователя указать сразу access_token and token_secret) twitter_auth.py:
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

Для установки twitter библиотеки нужно выполнить 
pip install requirements.txt