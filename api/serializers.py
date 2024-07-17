from rest_framework import serializers
from accounts.models import Account
from forum.models import Forum, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')

class UserForForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class CategoryForForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ForumSerializer(serializers.ModelSerializer):
    moderator = UserForForumSerializer()
    category = CategoryForForumSerializer()
    class Meta:
        model = Forum
        fields = ('id', 'forum_question', 'forum_about', 'category', 'forum_image', 'status', 'forum_views', 'moderator', 'created_at', 'updated_at')


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

