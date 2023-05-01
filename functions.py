from datetime import datetime, timedelta


def format_social_media_post_time(post_time):
    current_time = datetime.now()
    time_difference = current_time - post_time

    years = time_difference.days // 365
    if years > 0:
        if years == 1:
            return "a year ago"
        return f"{years} years ago"

    months = time_difference.days // 30
    if months > 0:
        if months == 1:
            return "a month ago"
        return f"{months} months ago"

    weeks = time_difference.days // 7
    if weeks > 0:
        if weeks == 1:
            return "a week ago"
        return f"{weeks} weeks ago"

    days = time_difference.days
    if days > 0:
        if days == 1:
            return "a day ago"
        return f"{days} days ago"

    hours = time_difference.seconds // 3600
    if hours > 0:
        if hours == 1:
            return "an hour ago"
        return f"{hours} hours ago"

    minutes = time_difference.seconds // 60
    if minutes > 0:
        if minutes == 1:
            return "a minute ago"
        return f"{minutes} minutes ago"

    seconds = time_difference.seconds
    if seconds == 1:
        return "a second ago"
    return f"{seconds} seconds ago"
