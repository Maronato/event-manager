from model_sockets.subscriptions import base


class BaseTeamSubscription(base.BaseSubscriptionReceiver):
    """Allows team members to track team updates

    Teams are fetched with relation to its id
    """

    sub_type = "publish.subscription"

    def get_group_name(self):
        return f'team_sub_{self.instance.id}{"".join([f"_{arg}" for arg in self.volatile_args])}'

    def is_valid(self):
        """Whether or not the update
        is valid. That is, if it is allowed
        """
        if not super().is_valid():
            return False
        return True


class CreateTeamSubscription(BaseTeamSubscription):
    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept created signals
        if not kwargs["created"]:
            return

        instance = kwargs["instance"]
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class UpdateTeamSubscription(BaseTeamSubscription):
    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept updated signals
        if kwargs["created"]:
            return
        instance = kwargs["instance"]
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class DeleteTeamSubscription(BaseTeamSubscription):
    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        instance = kwargs["instance"]
        self.data = {"id": getattr(instance, "id", None)}
        self.dispatch()
