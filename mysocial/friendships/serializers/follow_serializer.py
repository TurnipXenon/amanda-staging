from rest_framework import serializers

from authors.serializers.author_serializer import AuthorSerializer
from friendships.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.SerializerMethodField('get_summary')
    target = AuthorSerializer(read_only=True)
    actor = AuthorSerializer(read_only=True)

    def get_type(self, model):
        return model.get_serializer_field_name()

    def get_summary(self, model):
        return str(model)

    class Meta:
        model = Follow
        # todo(turnip): url, host, profile image
        fields = ('type', 'summary', 'is_pending', 'target', 'actor')
