import pandas as pd
import numpy as np
import nltk

def dream_preprocess(file:str, min_post: int, min_comment:int)->pd.DataFrame:
    dreams_raw = pd.read_csv(file)
    dreams_raw.dropna(subset=['comment_id', 'comment_text','post_text', 'post_id'], inplace=True)
    dreams = dreams_raw.drop_duplicates(subset='comment_id')
    dreams = dreams[dreams['user_id']!= dreams['commenter_id']]
    posts = pd.DataFrame(dreams['post_text'].drop_duplicates())
    posts['length']=posts['post_text'].apply(lambda x: len(nltk.word_tokenize(x)))
    dreams['length_post']=dreams['post_text'].apply(lambda x: len(nltk.word_tokenize(x)))
    dreams['length_comment']=dreams['comment_text'].apply(lambda x: len(nltk.word_tokenize(x)))
    dreams = dreams[(dreams['length_post']>= min_post) & (dreams['length_comment']>=min_comment)]
    columns_relevant = ['user_id', 'post_text', 'post_time', 'likes', 'comments', 'comment_id', 'commenter_id', 'comment_text', 'comment_time', 'length_post', 'length_comment']
    return dreams[columns_relevant]