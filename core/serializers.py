from djoser.serializers import UserCreateSerializer as BaseUserUserCreateSerializer

class UserCreateSerializer(BaseUserUserCreateSerializer):
  class Meta(BaseUserUserCreateSerializer.Meta):
    fields = ['id','username','password','email','first_name','last_name']