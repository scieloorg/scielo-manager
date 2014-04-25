from django.db.models import DateTimeField


def safe_autodatetime(modelname):
    """
    Decorator to be used in migrations. This decorator monkeypatch a given
    model to avoid the datetimefield to override the current dates
    priviously registered in the database.
    """
    def rewrapper(func):

        def wrapper(instance, orm):

            attr = getattr(orm, modelname)

            fields = [field for field in attr._meta.fields if isinstance(
                field, DateTimeField
            )]

            for field in fields:
                field.auto_now_add = False
                field.auto_now = False

            return func(instance, orm)

        return wrapper

    return rewrapper
