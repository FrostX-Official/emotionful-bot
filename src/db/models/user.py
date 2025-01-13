from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.BigIntField(primary_key=True)
    username = fields.CharField(max_length=32, null=True)

    stars = fields.BigIntField()
    stickerpacks = fields.ReverseRelation["StickerPack"]

class StickerPack(Model):
    id = fields.BigIntField(primary_key=True)
    title = fields.CharField(max_length=64)
    short_name = fields.CharField(max_length=64)

    creator = fields.ForeignKeyField(model_name="models.User", related_name="stickerpacks")

    sticker_count = fields.IntField()