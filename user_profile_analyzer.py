import re
import datetime
from difflib import SequenceMatcher
from statistics import mean

def get_name_similarity_score(user):
    name = user.name
    screen_name = user.screen_name
    if 'bot' in name.lower() or 'bot' in screen_name.lower():
        return 1
    return 1 - SequenceMatcher(None, name, screen_name).ratio()

def get_name_length_score(user):
    name_length = len(user.name)
    if name_length > 15:
        name_length_score = name_length * 0.009
        return 1 if name_length_score > 1 else name_length_score
    else:
        return 0.15

def get_screen_name_length_score(user):
    screen_name_length = len(user.screen_name)
    if screen_name_length > 10:
        screen_name_length_score = screen_name_length * 0.012
        return 1 if screen_name_length_score > 1 else screen_name_length_score
    else:
        return 0.15

def get_screen_name_generated_score(user):
    screen_name = user.screen_name
    number_of_digits = len(screen_name) - len(re.sub(r'\d+', '', screen_name))
    if number_of_digits > 2:
        screen_name_generated_score = number_of_digits * 0.12
        return 1 if screen_name_generated_score > 1 else screen_name_generated_score
    else:
        return 0.15

def get_description_length_score(user):
    description_length = len(user.description)
    if description_length < 10:
        description_length_score = 1 - (description_length * 0.1)
        return 0 if description_length_score < 0 else description_length_score
    else:
        return 0.15

def get_user_age_in_days(user):
    created_at = user.created_at
    current_date = datetime.datetime.utcnow()
    user_age = current_date - created_at
    return user_age.days

def get_user_age_score(user):
    user_age = get_user_age_in_days(user)
    if user_age > 90:
        user_age_score = 1 - (user_age * 0.001)
        return 0 if user_age_score < 0 else user_age_score
    else:
        return 1

def get_tweet_ratio_score(user):
    number_of_tweets = user.statuses_count
    user_age = get_user_age_in_days(user)
    tweet_ratio = number_of_tweets / user_age
    return tweet_ratio * 0.05

def get_favorite_score(user):
    number_of_favorites = user.favourites_count
    favorite_score = 1 - (number_of_favorites * 0.01)
    return 0 if favorite_score < 0 else favorite_score

def get_profile_image_score(user):
    return 1 if user.default_profile_image else 0.15

def is_verified(user):
    return user.verified

def get_user_score(user):
    if is_verified(user):
        return 0
    
    scores = []
    scores.append(get_name_similarity_score(user))
    scores.append(get_name_length_score(user))
    scores.append(get_screen_name_length_score(user))
    scores.append(get_screen_name_generated_score(user))
    scores.append(get_description_length_score(user))
    scores.append(get_user_age_score(user))
    scores.append(get_tweet_ratio_score(user))
    scores.append(get_favorite_score(user))
    scores.append(get_profile_image_score(user))
    user_score = mean(scores)
    
    if user_score < 0:
        user_score = 0
    if user_score > 1:
        user_score = 1
    
    return user_score