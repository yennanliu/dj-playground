import typing
from collections import OrderedDict

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import fields, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from pydis_site.apps.api.models.bot.infraction import Infraction
from pydis_site.apps.api.models.bot.metricity import Metricity, NotFoundError
from pydis_site.apps.api.models.bot.user import User
from pydis_site.apps.api.serializers import UserSerializer


class UserListPagination(PageNumberPagination):
    """Custom pagination class for the User Model."""

    page_size = 2500
    page_size_query_param = "page_size"

    def get_next_page_number(self) -> typing.Optional[int]:
        """Get the next page number."""
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_page_number(self) -> typing.Optional[int]:
        """Get the previous page number."""
        if not self.page.has_previous():
            return None

        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data: list) -> Response:
        """Override method to send modified response."""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next_page_no', self.get_next_page_number()),
            ('previous_page_no', self.get_previous_page_number()),
            ('results', data)
        ]))


class UserViewSet(ModelViewSet):
    """
    View providing CRUD operations on Discord users through the bot.

    ## Routes
    ### GET /bot/users
    Returns all users currently known with pagination.

    #### Response format
    >>> {
    ...     'count': 95000,
    ...     'next_page_no': "2",
    ...     'previous_page_no': None,
    ...     'results': [
    ...      {
    ...         'id': 409107086526644234,
    ...         'name': "Python",
    ...         'discriminator': 4329,
    ...         'roles': [
    ...             352427296948486144,
    ...             270988689419665409,
    ...             277546923144249364,
    ...             458226699344019457
    ...         ],
    ...         'in_guild': True
    ...     },
    ...     ]
    ... }

    #### Optional Query Parameters
    - username: username to search for
    - discriminator: discriminator to search for
    - page_size: number of Users in one page, defaults to 10,000
    - page: page number

    #### Status codes
    - 200: returned on success

    ### GET /bot/users/<snowflake:int>
    Gets a single user by ID.

    #### Response format
    >>> {
    ...     'id': 409107086526644234,
    ...     'name': "Python",
    ...     'discriminator': 4329,
    ...     'roles': [
    ...         352427296948486144,
    ...         270988689419665409,
    ...         277546923144249364,
    ...         458226699344019457
    ...     ],
    ...     'in_guild': True
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### GET /bot/users/<snowflake:int>/metricity_data
    Gets metricity data for a single user by ID.

    #### Response format
    >>> {
    ...    "joined_at": "2020-10-06T21:54:23.540766",
    ...    "total_messages": 2,
    ...    "voice_banned": False,
    ...    "activity_blocks": 1
    ...}

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### GET /bot/users/<snowflake:int>/metricity_review_data
    Gets metricity data for a single user's review by ID.

    #### Response format
    >>> {
    ...     'joined_at': '2020-08-26T08:09:43.507000',
    ...     'top_channel_activity': [['off-topic', 15],
    ...                              ['talent-pool', 4],
    ...                              ['defcon', 2]],
    ...     'total_messages': 22
    ... }

    #### Status codes
    - 200: returned on success
    - 404: if a user with the given `snowflake` could not be found

    ### POST /bot/users/metricity_activity_data
    Returns a mapping of user ID to message count in a given period for
    the given user IDs.

    #### Required Query Parameters
    - days: how many days into the past to count message from.

    #### Request Format
    >>> [
    ...     409107086526644234,
    ...     493839819168808962
    ... ]

    #### Response format
    >>> {
    ...     "409107086526644234": 54,
    ...     "493839819168808962": 0
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if request body or query parameters were missing or invalid

    ### POST /bot/users
    Adds a single or multiple new users.
    The roles attached to the user(s) must be roles known by the site.
    Users that already exist in the database will be skipped.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    Alternatively, request users can be POSTed as a list of above objects,
    in which case multiple users will be created at once. In this case,
    the response is an empty list.

    #### Status codes
    - 201: returned on success
    - 400: if one of the given roles does not exist, or one of the given fields is invalid
    - 400: if multiple user objects with the same id are given

    ### PUT /bot/users/<snowflake:int>
    Update the user with the given `snowflake`.
    All fields in the request body are required.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### PATCH /bot/users/<snowflake:int>
    Update the user with the given `snowflake`.
    All fields in the request body are optional.

    #### Request body
    >>> {
    ...     'id': int,
    ...     'name': str,
    ...     'discriminator': int,
    ...     'roles': List[int],
    ...     'in_guild': bool
    ... }

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 404: if the user with the given `snowflake` could not be found

    ### BULK PATCH /bot/users/bulk_patch
    Update users with the given `ids` and `details`.
    `id` field and at least one other field is mandatory.

    #### Request body
    >>> [
    ...     {
    ...         'id': int,
    ...         'name': str,
    ...         'discriminator': int,
    ...         'roles': List[int],
    ...         'in_guild': bool
    ...     },
    ...     {
    ...         'id': int,
    ...         'name': str,
    ...         'discriminator': int,
    ...         'roles': List[int],
    ...         'in_guild': bool
    ...     },
    ... ]

    #### Status codes
    - 200: returned on success
    - 400: if the request body was invalid, see response body for details
    - 400: if multiple user objects with the same id are given
    - 404: if the user with the given id does not exist

    ### DELETE /bot/users/<snowflake:int>
    Deletes the user with the given `snowflake`.

    #### Status codes
    - 204: returned on success
    - 404: if a user with the given `snowflake` does not exist
    """

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("id")
    pagination_class = UserListPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'discriminator')

    def get_serializer(self, *args, **kwargs) -> ModelSerializer:
        """Set Serializer many attribute to True if request body contains a list."""
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=["PATCH"], name='user-bulk-patch')
    def bulk_patch(self, request: Request) -> Response:
        """Update multiple User objects in a single request."""
        serializer = self.get_serializer(
            instance=self.get_queryset(),
            data=request.data,
            many=True,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def metricity_data(self, request: Request, pk: str = None) -> Response:
        """Request handler for metricity_data endpoint."""
        user = self.get_object()

        has_voice_infraction = Infraction.objects.filter(
            Q(user__id=user.id, active=True),
            Q(type="voice_ban") | Q(type="voice_mute")
        ).exists()

        with Metricity() as metricity:
            try:
                data = metricity.user(user.id)

                data["total_messages"] = metricity.total_messages(user.id)
                data["activity_blocks"] = metricity.total_message_blocks(user.id)

                data["voice_gate_blocked"] = has_voice_infraction
                return Response(data, status=status.HTTP_200_OK)
            except NotFoundError:
                return Response(dict(detail="User not found in metricity"),
                                status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def metricity_review_data(self, request: Request, pk: str = None) -> Response:
        """Request handler for metricity_review_data endpoint."""
        user = self.get_object()

        with Metricity() as metricity:
            try:
                data = metricity.user(user.id)
                data["total_messages"] = metricity.total_messages(user.id)
                data["top_channel_activity"] = metricity.top_channel_activity(user.id)
                return Response(data, status=status.HTTP_200_OK)
            except NotFoundError:
                return Response(dict(detail="User not found in metricity"),
                                status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["POST"])
    def metricity_activity_data(self, request: Request) -> Response:
        """Request handler for metricity_activity_data endpoint."""
        if "days" in request.query_params:
            try:
                days = int(request.query_params["days"])
            except ValueError:
                raise ParseError(detail={
                    "days": ["This query parameter must be an integer."]
                })
        else:
            raise ParseError(detail={
                "days": ["This query parameter is required."]
            })

        user_id_list_validator = fields.ListField(
            child=fields.IntegerField(min_value=0),
            allow_empty=False
        )
        user_ids = [
            str(user_id) for user_id in
            user_id_list_validator.run_validation(request.data)
        ]

        with Metricity() as metricity:
            data = metricity.total_messages_in_past_n_days(user_ids, days)

        default_data = {user_id: 0 for user_id in user_ids}
        response_data = default_data | dict(data)
        return Response(response_data, status=status.HTTP_200_OK)
