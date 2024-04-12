from rest_framework.throttling import UserRateThrottle


class FriendRequestThrottleRate(UserRateThrottle):
    """ 
    User can only send 3 request in a minute
    """
    rate = '3/min'