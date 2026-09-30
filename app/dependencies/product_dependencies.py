from fastapi import Depends
from app.config_db.session import get_db
from app.services.product_service import ProductService
from app.repositories.product_repo import ProductRepo


# It is a dependency provider: a small factory function that assembles the objects needed to work with products. 
# The important part is that the repository and service share the same db session. The repository uses it to read and write
#  product records; the service uses it to commit successful changes or roll them back if something fails.
# In this project, get_db_session creates a session, yields it to the request, and closes it when the request finishes. 
# That gives the repository and service a session to use for that request without each controller having to remember 
# to create and close one. FastAPI also normally reuses the result of the same dependency within a single request, 
# rather than creating a fresh session every time the dependency appears in that request’s dependency graph.

# We have to call get_product_service() in the controller to get a ProductService instance. 

def get_product_service(db = Depends(get_db)) -> ProductService: 
    repo = ProductRepo(db)
    return ProductService(repo,db)