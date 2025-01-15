from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.BigIntField(primary_key=True)
    username = fields.CharField(max_length=32, null=True)

    stars = fields.BigIntField()

    stickerpacks = fields.ReverseRelation["StickerPack"]
    emojipacks = fields.ReverseRelation["EmojiPack"]

class StickerPack(Model):
    id = fields.BigIntField(primary_key=True)
    title = fields.CharField(max_length=64)
    short_name = fields.CharField(max_length=64)

    creator = fields.ForeignKeyField(model_name="models.User", related_name="stickerpacks")

    count = fields.IntField()

class EmojiPack(Model):
    id = fields.BigIntField(primary_key=True)
    title = fields.CharField(max_length=64)
    short_name = fields.CharField(max_length=64)

    creator = fields.ForeignKeyField(model_name="models.User", related_name="emojipacks")

    count = fields.IntField()