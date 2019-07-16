from model_sockets.consumers import ModelSignalConsumer
from channels.db import database_sync_to_async
from .models import Team


class TeamSignalConsumer(ModelSignalConsumer):
    """Consumer that tracks individual teams"""

    async def get_team_id(self):
        return self.scope["url_route"]["kwargs"]["team_id"]

    async def get_app_model(self):
        return Team

    @database_sync_to_async
    async def get_user_is_allowed(self, user):
        return Team.is_team_member(await self.get_team_id(), user)

    async def get_model_is_allowed(self, model_class):
        return True

    async def get_signal_group_name(self):
        team_id = await self.get_team_id()
        signal = await self.get_signal_type()
        return f"team_sub_{team_id}_{signal}"
