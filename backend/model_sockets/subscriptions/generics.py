from .base import BaseSubscriptionReceiver, BaseInstanceUpdateReceiver
from django.conf import settings


class UniversalReceiver(BaseSubscriptionReceiver):
    def get_group_name(self, *args, **kwargs):
        # Get group name used to dispatch messages
        return f"sub_{self.sender._meta.app_label}_{self.sender.__name__}_universal"


class CreateReceiver(UniversalReceiver):

    signal_name = "create"

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept created signals
        if not kwargs["created"]:
            return

        instance = kwargs["instance"]
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class UpdateReceiver(UniversalReceiver):

    signal_name = "update"

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept updated signals
        if kwargs["created"]:
            return
        instance = kwargs["instance"]
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class DeleteReceiver(UniversalReceiver):

    signal_name = "delete"

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        instance = kwargs["instance"]
        self.data = {"id": getattr(instance, "id", None)}
        self.dispatch()


class M2MAddReceiver(UniversalReceiver):

    signal_name = "m2m_add"

    def receive(self, sender, **kwargs):
        print("receiving add")
        super().receive(sender, **kwargs)
        action = kwargs["action"]
        if action != "post_add":
            return
        instance = kwargs["instance"]
        self.data = self.get_instance_fields(instance.__class__, instance)
        self.dispatch()
        print()

    def is_valid(self):
        if not getattr(self.instance.__class__, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    @property
    def group_name(self):
        return f"sub_{self.sender._meta.app_label}_{self.instance.__class__.__name__}_universal"


class M2MRemoveReceiver(UniversalReceiver):

    signal_name = "m2m_remove"

    def receive(self, sender, **kwargs):
        print("receiving remove")
        super().receive(sender, **kwargs)
        action = kwargs["action"]
        if action != "post_remove":
            return
        instance = kwargs["instance"]
        self.data = {"id": getattr(instance, "id", None)}
        self.dispatch()
        print()

    def is_valid(self):
        if not getattr(self.instance.__class__, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    @property
    def group_name(self):
        return f"sub_{self.sender._meta.app_label}_{self.instance.__class__.__name__}_universal"


class M2MClearReceiver(UniversalReceiver):

    signal_name = "m2m_clear"

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        action = kwargs["action"]
        if action != "post_clear":
            return
        instance = kwargs["instance"]
        self.data = {"id": getattr(instance, "id", None)}
        self.dispatch()

    def is_valid(self):
        if not getattr(self.instance.__class__, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    @property
    def group_name(self):
        return f"sub_{self.sender._meta.app_label}_{self.instance.__class__.__name__}_universal"


class SelfUserUpdateReceiver(BaseInstanceUpdateReceiver):
    def get_allowed_serializer_class(self, path=None):
        # Self subscription fields are to be different from
        # regular updates from the same model

        return super().get_allowed_serializer_class(
            settings.MSOCKS_SELF_SUBSCRIPTION_SERIALIZER
        )

    def is_valid(self):
        """Self subscriptions ignore the model's allow field"""
        if not settings.MSOCKS_ALLOW_SELF_SUBSCRIPTION:
            # This model does not allow subscriptions
            return False
        return True
