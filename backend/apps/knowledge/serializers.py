from rest_framework import serializers

from .models import Entry, Tag

class TagBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")