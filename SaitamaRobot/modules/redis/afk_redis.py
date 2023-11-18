from SaitamaRobot import REDIS

# AFK
def is_user_afk(userid):
    """
    Check if a user is marked as AFK.

    Args:
        userid (int): User ID.

    Returns:
        bool: True if the user is AFK, False otherwise.
    """
    return bool(REDIS.get(f"is_afk_{userid}"))

def start_afk(userid, reason):
    """
    Mark a user as AFK.

    Args:
        userid (int): User ID.
        reason (str): AFK reason.

    Returns:
        None
    """
    REDIS.set(f"is_afk_{userid}", reason)

def afk_reason(userid):
    """
    Get the AFK reason for a user.

    Args:
        userid (int): User ID.

    Returns:
        str: AFK reason or None if the user is not AFK.
    """
    return REDIS.get(f"is_afk_{userid}").decode('utf-8') if is_user_afk(userid) else None

def end_afk(userid):
    """
    End a user's AFK status.

    Args:
        userid (int): User ID.

    Returns:
        bool: True if the user was AFK and is now marked as not AFK, False otherwise.
    """
    key = f"is_afk_{userid}"
    if is_user_afk(userid):
        REDIS.delete(key)
        return True
    return False

# Helpers
def strb(redis_string):
    """
    Convert a Redis byte string to a decoded string.

    Args:
        redis_string (bytes): Redis byte string.

    Returns:
        str: Decoded string or None if the input is None.
    """
    return redis_string.decode('utf-8') if redis_string else None
