from typing import List, Tuple

from django.db import connections

BLOCK_INTERVAL = 10 * 60  # 10 minute blocks

EXCLUDE_CHANNELS = (
    "267659945086812160",  # Bot commands
    "607247579608121354"  # SeasonalBot commands
)


class NotFoundError(Exception):  # noqa: N818
    """Raised when an entity cannot be found."""

    pass


class Metricity:
    """Abstraction for a connection to the metricity database."""

    def __init__(self):
        self.cursor = connections['metricity'].cursor()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.cursor.close()

    def user(self, user_id: str) -> dict:
        """Query a user's data."""
        # TODO: Swap this back to some sort of verified at date
        columns = ["joined_at"]
        query = f"SELECT {','.join(columns)} FROM users WHERE id = '%s'"
        self.cursor.execute(query, [user_id])
        values = self.cursor.fetchone()

        if not values:
            raise NotFoundError()

        return dict(zip(columns, values))

    def total_messages(self, user_id: str) -> int:
        """Query total number of messages for a user."""
        self.cursor.execute(
            """
            SELECT
                COUNT(*)
            FROM messages
            WHERE
                author_id = '%s'
                AND NOT is_deleted
                AND channel_id NOT IN %s
            """,
            [user_id, EXCLUDE_CHANNELS]
        )
        values = self.cursor.fetchone()

        if not values:
            raise NotFoundError()

        return values[0]

    def total_message_blocks(self, user_id: str) -> int:
        """
        Query number of 10 minute blocks during which the user has been active.

        This metric prevents users from spamming to achieve the message total threshold.
        """
        self.cursor.execute(
            """
            SELECT
                COUNT(*)
            FROM (
                SELECT
                    (floor((extract('epoch' from created_at) / %s )) * %s) AS interval
                FROM messages
                WHERE
                    author_id='%s'
                    AND NOT is_deleted
                    AND channel_id NOT IN %s
                GROUP BY interval
            ) block_query;
            """,
            [BLOCK_INTERVAL, BLOCK_INTERVAL, user_id, EXCLUDE_CHANNELS]
        )
        values = self.cursor.fetchone()

        if not values:
            raise NotFoundError()

        return values[0]

    def top_channel_activity(self, user_id: str) -> List[Tuple[str, int]]:
        """
        Query the top three channels in which the user is most active.

        Help channels are grouped under "the help channels",
        and off-topic channels are grouped under "off-topic".
        """
        self.cursor.execute(
            """
            SELECT
                CASE
                    WHEN channels.name ILIKE 'help-%%' THEN 'the help channels'
                    WHEN channels.name ILIKE 'ot%%' THEN 'off-topic'
                    WHEN channels.name ILIKE '%%voice%%' THEN 'voice chats'
                    ELSE channels.name
                END,
                COUNT(1)
            FROM
                messages
                LEFT JOIN channels ON channels.id = messages.channel_id
            WHERE
                author_id = '%s' AND NOT messages.is_deleted
            GROUP BY
                1
            ORDER BY
                2 DESC
            LIMIT
                3;
            """,
            [user_id]
        )

        values = self.cursor.fetchall()

        if not values:
            raise NotFoundError()

        return values

    def total_messages_in_past_n_days(
        self,
        user_ids: list[str],
        days: int
    ) -> list[tuple[str, int]]:
        """
        Query activity by a list of users in the past `days` days.

        Returns a list of (user_id, message_count) tuples.
        """
        self.cursor.execute(
            """
            SELECT
                author_id, COUNT(*)
            FROM messages
            WHERE
                author_id IN %s
                AND NOT is_deleted
                AND channel_id NOT IN %s
                AND created_at > now() - interval '%s days'
            GROUP BY author_id
            """,
            [tuple(user_ids), EXCLUDE_CHANNELS, days]
        )
        values = self.cursor.fetchall()

        return values
