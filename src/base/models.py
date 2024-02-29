from tortoise import fields
from tortoise.manager import Manager
from tortoise.models import Model


class StatusManager(Manager):
    def get_queryset(self):
        return super(StatusManager, self).get_queryset().filter(deleted=False)


class ModelBase(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DateTimeField(auto_now_add=True)
    updated_at = fields.DateTimeField(auto_now=True)
    deleted = fields.BooleanField(default=False)
    # all_objects = Manager()

    async def delete(self) -> None:
        """
        We don't delete the record, we just mark it as deleted.
        """
        self.deleted = True
        await self.save()

    class Meta:
        manager = StatusManager()
