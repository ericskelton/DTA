from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Snippet, CustomUser



class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    
    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']

class CustomUserSerializer(serializers.Serializer):
    # def update(self, instance, validated_data):
        

    #     return super().update(instance, validated_data)
    # def validate_amout(self, value):
    #     if not isinstance(value, int):
    #         raise serializers.ValidationError("amount must be an integer")
    #     sel
    #     return value
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'balance']

class ADDSerializer(serializers.HyperlinkedModelSerializer):
    # user_id = serializers.HyperlinkedRelatedField(many=True, view_name='user-id', read_only=True)
    amount = serializers.HyperlinkedRelatedField(many=True, view_name='amount', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'balance']