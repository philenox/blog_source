# db_router.py
import logging
logger = logging.getLogger(__name__)

class RecipesRouter:
    """
    A router to control all database operations on models in the recipes app.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read recipes models go to recipes_db.
        """
        if model._meta.app_label == 'recipes':
            return 'recipes_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write recipes models go to recipes_db.
        """
        if model._meta.app_label == 'recipes':
            return 'recipes_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the recipes app is involved.
        """
        if obj1._meta.app_label == 'recipes' or \
           obj2._meta.app_label == 'recipes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the recipes app only appears in the 'recipes_db' database,
        and other apps do not migrate to 'recipes_db'.
        """
        if app_label == 'recipes':
            return db == 'recipes_db'
        elif db == 'recipes_db':
            return False  # Prevent other apps from migrating to 'recipes_db'
        logger.debug(f"allow_migrate({db}, {app_label}): None (default behavior)")
        return None