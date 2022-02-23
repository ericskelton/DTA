from api.utils.log import logError
from rest_framework import status
from rest_framework.response import Response

def handleViewError(exception, request):
    """
    Handles a view error.
    """
    logError(exception, request)
    statuses = {
        'UserNotFound': status.HTTP_404_NOT_FOUND,
        'UserAlreadyExists': status.HTTP_409_CONFLICT,
        'InvalidRequest': status.HTTP_400_BAD_REQUEST,
        'InsufficientFunds': status.HTTP_400_BAD_REQUEST,
        'InvalidTicker': status.HTTP_400_BAD_REQUEST,
        'InvalidTransaction': status.HTTP_400_BAD_REQUEST,
        'InvalidTransactionType': status.HTTP_400_BAD_REQUEST,
        'InvalidTransactionStatus': status.HTTP_400_BAD_REQUEST,
        'NotEnoughFunds': status.HTTP_400_BAD_REQUEST,
        'InvalidUser': status.HTTP_400_BAD_REQUEST,
        'InvalidUserStatus': status.HTTP_400_BAD_REQUEST,
    }
    return Response(
        {'error': exception.args[0]},
        status= statuses[exception.args[0]] if exception.args[0] in statuses else status.HTTP_400_BAD_REQUEST
    )