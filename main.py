import redis


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)



def add_recipe(recipe_data):
   
# crear ID 

    recipe_id = redis_client.incr("recipe_id")  
    redis_client.hset(f"recipe:{recipe_id}", mapping=recipe_data)
    return recipe_id


def search_recipes(search_term):
   

    recipes = []
    for key in redis_client.scan_iter("recipe:*"):
        recipe_data = redis_client.hgetall(key).decode("utf-8")  
        if search_term.lower() in recipe_data.lower():
            recipes.append(eval(recipe_data))  
    return recipes


def get_recipe(recipe_id):
    

    key = f"recipe:{recipe_id}"
    if not redis_client.exists(key):
        return None
    recipe_data = redis_client.hgetall(key).decode("utf-8")
    return eval(recipe_data) 


def update_recipe(recipe_id, update_data):
   

    key = f"recipe:{recipe_id}"
    if not redis_client.exists(key):
        return 0
    redis_client.hset(key, mapping=update_data)
    return 1


def delete_recipe(recipe_id):
   

    key = f"recipe:{recipe_id}"
    return redis_client.delete(key)


if __name__ == "__main__":
    recipe_id = add_recipe(
        {
            "nombre": "Pizza Margharita",
            "ingredients": ["masa", "salsa ", "Mozzarella "],
            
    
            
        }
    )
    print(f"agregar receta con  ID: {recipe_id}")

    search_results = search_recipes("cheese")
    print(f"\nreceta con  'cheese':")
    for recipe in search_results:
        print(recipe["nombre"])

    updated_count = update_recipe(recipe_id, {"": [""]})
    print(f"\nactualizar receta: {updated_count} " )

    deleted_count = delete_recipe(recipe_id)  # Adjust recipe_id for deletion
    print(f"\nborrar receta : {deleted_count} " )
