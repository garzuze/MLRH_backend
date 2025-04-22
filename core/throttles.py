from rest_framework.throttling import AnonRateThrottle

class SignupRateThrottle(AnonRateThrottle):
    rate = '5/hour'