from django.db import models
from django.db.models.signals import post_save, post_delete
from settings.models import Settings
from .subscriptions import team_subscription


class Team(models.Model):
    msocks_allow = True
    msocks_fields = [
        'id',
        'name',
        'description',
        'location',
        'members',
        'project_url',
        'allow_new'
    ]

    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256, blank=True)
    location = models.CharField(max_length=32, blank=True)
    project_url = models.URLField(blank=True)
    allow_new = models.BooleanField(default=True)

    @property
    def members(self):
        return list(self.hackers.all().values_list('profile__shortcuts__full_name', flat=True))

    @property
    def is_full(self):
        max_team_size = Settings.get().max_team_size
        return max_team_size != 0 and len(self.members) >= max_team_size

    def add_hacker(self, hacker):
        self.hackers.add(hacker)
        post_save.send(Team, instance=self, created=False)

    def remove_hacker(self, hacker):
        self.hackers.remove(hacker)
        post_save.send(Team, instance=self, created=False)

    @classmethod
    def is_team_member(cls, team_id, user):
        return cls.objects.filter(id=team_id).filter(hackers__in=[user.profile.hacker]).exists()


mapper = {
    'create': (team_subscription.CreateTeamSubscription, post_save),
    'update': (team_subscription.UpdateTeamSubscription, post_save),
    'delete': (team_subscription.DeleteTeamSubscription, post_delete)
}

for event in mapper.keys():
    # Register ticket subscriptions
    reg = mapper[event][0](mapper[event][1], event)
    reg.register(Team)
