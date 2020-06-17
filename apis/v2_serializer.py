from accounts.models import User
from contents.models import Comment
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #field = '__all__'
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'image', 'message',)
        # exclude = ('is_active', 'password', 'is_admin', 'created_date', 'modified_date')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    # field = '__all__'
    # content = serializers.StringRelatedField(many=False)
    user = UserSerializer(many=False, read_only=True)
    # user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'created_at', 'user')

class CommentReverseSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
    
        fields = ('id', 'comment', 'created_at', 'user')
    