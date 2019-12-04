import tweepy


def get_hashtag_score(tweets):
    hashtag_data = {}
    for tweet in tweets:
        for hashtag in tweet.entities['hashtags']:
            hashtag_text = hashtag['text']
            if hashtag_text not in hashtag_data.keys():
                hashtag_data[hashtag_text] = 1
            else:
                hashtag_data[hashtag_text] += 1

    hashtag_score = 0 if sum(
        hashtag_data.values()) == 0 else 1 - (len(hashtag_data.keys()) /
                                              sum(hashtag_data.values()))

    return hashtag_score, sum(hashtag_data.values())


def get_user_mention_score(tweets):
    user_mention_data = {}
    for tweet in tweets:
        for user_mention in tweet.entities['user_mentions']:
            mentioned_screen_name = user_mention['screen_name']
            if mentioned_screen_name == tweet.in_reply_to_screen_name:
                continue
            if mentioned_screen_name not in user_mention_data.keys():
                user_mention_data[mentioned_screen_name] = 1
            else:
                user_mention_data[mentioned_screen_name] += 1

    user_mention_score = 0 if sum(user_mention_data.values()) == 0 else 1 - (
        len(user_mention_data.keys()) / sum(user_mention_data.values()))
    
    return user_mention_score, sum(user_mention_data.values())


def get_timeline_score(tweets):
    hashtag_score, hashtag_count = get_hashtag_score(tweets)
    user_mention_score, user_mention_count = get_user_mention_score(tweets)

    entities_count = hashtag_count + user_mention_count
    avg_entities = entities_count / (len(tweets) * 2)

    if avg_entities > 2:
        avg_entities /= 2
    elif avg_entities > 1:
        avg_entities = 1

    tweets_score = avg_entities + ((hashtag_score + user_mention_score) / 2)

    return tweets_score
