'''Serializers for recipe APIs'''

from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields =['id']
        

class RecipeSerializer(serializers.ModelSerializer):
    '''Serilizer for recipes'''
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user #use context coz we use serializer
        for tag in tags:
            tag_obj, createad = Tag.objects.get_or_create(
                user=auth_user,
                **tag, #get all the values in the tag instead of name = name['tag']
            )
            recipe.tags.add(tag_obj)


    def create(self, validated_data):
        """Create a recipe"""
        tags = validated_data.pop('tags',[]) #remove the tag before we create recipe
        recipe = Recipe.objects.create(**validated_data) 
        self._get_or_create_tags(tags, recipe)
        
        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None) 
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    '''Serializer for recipe detail view.'''
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


