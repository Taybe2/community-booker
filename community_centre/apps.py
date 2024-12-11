from django.apps import AppConfig


class CommunityCentreConfig(AppConfig):
    """
    Provides primary key type for community_centre app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community_centre'
