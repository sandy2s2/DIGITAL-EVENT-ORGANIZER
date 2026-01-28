"""
Routes Package
Contains all Flask blueprints for routing
"""

from . import user_routes, admin_routes, event_routes, payment_routes

__all__ = ['user_routes', 'admin_routes', 'event_routes', 'payment_routes']
