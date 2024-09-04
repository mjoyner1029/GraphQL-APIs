# schema.py
from graphene import ObjectType, String, Float, Int, List, Field, Mutation, Schema, Boolean
from graphene import InputObjectType

# Define the Product type
class ProductType(ObjectType):
    id = Int()
    name = String()
    price = Float()
    quantity = Int()
    category = String()

# Define the Input type for adding or updating products
class ProductInput(InputObjectType):
    name = String(required=True)
    price = Float(required=True)
    quantity = Int(required=True)
    category = String()

# Sample in-memory storage for products
products_db = []
product_id_counter = 1

# Define the Query class
class Query(ObjectType):
    products = List(ProductType)
    product = Field(ProductType, id=Int(required=True))

    def resolve_products(self, info):
        return products_db

    def resolve_product(self, info, id):
        for product in products_db:
            if product['id'] == id:
                return product
        return None

# Define the Mutation class
class CreateProduct(Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = Field(ProductType)

    def mutate(self, info, input):
        global product_id_counter
        new_product = {
            'id': product_id_counter,
            'name': input.name,
            'price': input.price,
            'quantity': input.quantity,
            'category': input.category
        }
        products_db.append(new_product)
        product_id_counter += 1
        return CreateProduct(product=new_product)

class UpdateProduct(Mutation):
    class Arguments:
        id = Int(required=True)
        input = ProductInput(required=True)

    product = Field(ProductType)

    def mutate(self, info, id, input):
        for product in products_db:
            if product['id'] == id:
                product.update({
                    'name': input.name,
                    'price': input.price,
                    'quantity': input.quantity,
                    'category': input.category
                })
                return UpdateProduct(product=product)
        return None

class DeleteProduct(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(self, info, id):
        global products_db
        products_db = [product for product in products_db if product['id'] != id]
        return DeleteProduct(success=True)

# Define the schema
class Mutation(ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

schema = Schema(query=Query, mutation=Mutation)
