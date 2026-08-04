"""
API router configuration
Aggregates all API routers
"""

from fastapi import APIRouter

from app.api.endpoints import (
    auth,
    products,
    cart,
    orders,
    users,
    payments,
    reviews,
    search,
    agents,
    athena,
)

# Create main router
router = APIRouter()

# Include all endpoint routers
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(products.router, prefix="/products", tags=["Products"])
router.include_router(cart.router, prefix="/cart", tags=["Cart"])
router.include_router(orders.router, prefix="/orders", tags=["Orders"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(payments.router, prefix="/payments", tags=["Payments"])
router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
router.include_router(search.router, prefix="/search", tags=["Search"])
router.include_router(agents.router, prefix="/agents", tags=["AI Agents"])
router.include_router(athena.router, prefix="/athena", tags=["Project Athena"])

__all__ = ["router"]
