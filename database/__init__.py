import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_config(
        self, user_id: int, card_pool_id: str, player_id: str, record_id: str, server_id: str
    ) -> int:
        await self.connection.execute(
            "INSERT INTO ww_config(user_id, card_pool_id, player_id, record_id, server_id) VALUES (?, ?, ?, ?, ?)",
            (
                user_id,
                card_pool_id,
                player_id,
                record_id,
                server_id,
            ),
        )
        await self.connection.commit()
        return user_id

    async def remove_config(self, user_id: str) -> int:
        await self.connection.execute(
            "DELETE FROM ww_config WHERE user_id=?",
            (
                user_id,
            ),
        )

    async def get_configs(self, user_id: int) -> list:
        rows = await self.connection.execute(
            "SELECT user_id, card_pool_id, player_id, record_id, server_id, strftime('%s', created_at) FROM ww_config WHERE user_id=?",
            (
                user_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list
