import graphene
from graphene_django import DjangoObjectType

import decimal

from .models import Category, Product

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'

class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, id=graphene.Int())
    all_categories = graphene.List(CategoryType)

    product_by_id = graphene.Field(ProductType, id=graphene.Int())
    all_products = graphene.List(ProductType)
    product_by_name = graphene.List(ProductType, name=graphene.String(required=True))


    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Category.objects.get(pk=id)

        return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()


    def resolve_product_by_id(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Product.objects.get(pk=id)

        return None
    
    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()


    def resolve_product_by_name(self, info, **kwargs):
        name = kwargs.get('name')

        if name is not None:
            return Product.objects.filter(name=name)

        return None


class CreateCategory(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category()
        category.name = name
        category.save()

        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()

        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()

        return DeleteCategory(category=category)



class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    product_code= graphene.String()
    category = graphene.ID()
    quantity = graphene.Int()
    description = graphene.String()
    price = graphene.Float()
    category = graphene.ID()
    image = graphene.String()


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        input = ProductInput(required=True)

        
    @classmethod
    def mutate(cls, root, info, input):
        product = Product()
        product.product_code = input.product_code
        product.name = input.name
        product.product_code = input.product_code
        product.quantity = input.quantity
        product.description = input.description
        product.price = decimal.Decimal(input.price)
        product.category = Category.objects.get(id=input.category)
        product.image = input.image
        product.save()

        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        input = ProductInput(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        product = Product.objects.get(id=input.id)
        product.product_code = input.product_code
        product.name = input.name
        product.product_code = input.product_code
        product.quantity = input.quantity
        product.description = input.description
        product.price = decimal.Decimal(input.price)
        product.category = Category.objects.get(id=input.category)
        product.image = input.image
        product.save()

        return UpdateProduct(product=product)



class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)