from facebook_scraper import get_posts
import json
import pandas as pd
from tqdm import notebook
import os

posts = get_posts(group=161702467796939, credentials=('<insert-fb-username>','<insert-fb-password>'), 
					pages=100, options={"comments": True, "reactors": True, "progress": True, "posts_per_page": 4})

data = []
i=0 	# counter variable

for post in posts:
    data.append(post)
    i += 1
    print("Post count: %d" %(i))

results = pd.DataFrame(columns=['page_id','post_id','post_url','user_id','user_name','post_text','post_time',
								'likes','comments','shares','comment_id','comment_url','commenter_id','commenter_name',
								'comment_text','comment_time','reply_id','reply_url','replier_id','replier_name','reply_text','reply_time'])

post_list = []
comment_list = []
reply_list = []

for post in notebook.tqdm(data):
    
    post_details = [['']*10]
    
    post_details[0][0] = post.get('page_id', '')
    post_details[0][1] = post.get('post_id', '')
    post_details[0][2] = post.get('post_url', '')
    post_details[0][3] = post.get('user_id', '')
    post_details[0][4] = post.get('username', '')
    post_details[0][5] = post.get('text', '')
    post_details[0][6] = post.get('time', '')
    post_details[0][7] = post.get('likes', '')
    post_details[0][8] = len(post.get('comments_full',[]))
    post_details[0][9] = post.get('shares', '')

    post_comments = []
    post_replies = []
    
    for comment in post.get('comments_full',[]):
        comment_details = [['']*6]

        comment_details[0][0] = comment.get('comment_id', '')
        comment_details[0][1] = comment.get('comment_url', '')
        comment_details[0][2] = comment.get('commenter_id', '')
        comment_details[0][3] = comment.get('commenter_name', '')
        comment_details[0][4] = comment.get('comment_text', '')
        comment_details[0][5] = comment.get('comment_time', '')
        
        comment_replies = []
        for reply in comment.get('replies',[]):
            reply_details = [['']*6]

            reply_details[0][0] = reply.get('comment_id', '')
            reply_details[0][1] = reply.get('comment_url', '')
            reply_details[0][2] = reply.get('commenter_id', '')
            reply_details[0][3] = reply.get('commenter_name', '')
            reply_details[0][4] = reply.get('comment_text', '')
            reply_details[0][5] = reply.get('comment_time', '')
        
            comment_replies.extend(reply_details)
        
        if len(comment_replies)>1:
            comment_details = comment_details*len(comment_replies)
    
        if len(comment_replies)==0:
            comment_replies = [['']*6]
        
        post_comments.extend(comment_details)
        post_replies.extend(comment_replies)
        
    if len(post_replies)>1:
        post_details = post_details*len(post_replies)
    
    if len(post_comments)==0:
        post_replies = [['']*6]
        post_comments = [['']*6]
        
    reply_list.extend(post_replies)
    comment_list.extend(post_comments)
    post_list.extend(post_details)
    

results['page_id'] = [i[0] for i in post_list]
results['post_id'] = [i[1] for i in post_list]
results['post_url'] = [i[2] for i in post_list]
results['user_id'] = [i[3] for i in post_list]
results['user_name'] = [i[4] for i in post_list]
results['post_text'] = [i[5] for i in post_list]
results['post_time'] = [i[6] for i in post_list]
results['likes'] = [i[7] for i in post_list]
results['comments'] = [i[8] for i in post_list]
results['shares'] = [i[9] for i in post_list]
results['comment_id'] = [i[0] for i in comment_list]
results['comment_url'] = [i[1] for i in comment_list]
results['commenter_id'] = [i[2] for i in comment_list]
results['commenter_name'] = [i[3] for i in comment_list]
results['comment_text'] = [i[4] for i in comment_list]
results['comment_time'] = [i[5] for i in comment_list]
results['reply_id'] = [i[0] for i in reply_list]
results['reply_url'] = [i[1] for i in reply_list]
results['replier_id'] = [i[2] for i in reply_list]
results['replier_name'] = [i[3] for i in reply_list]
results['reply_text'] = [i[4] for i in reply_list]
results['reply_time'] = [i[5] for i in reply_list]


save_loc = './scraped_data'
if not os.path.exists(save_loc):
	os.makedirs(save_loc)
results.to_csv(save_loc+"/FB_scraped.csv", float_format='%f', index=False)
