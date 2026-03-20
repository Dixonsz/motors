def get_required_instance(model_class, object_id, error_message):
    """Obtiene una instancia por id o lanza ValueError con mensaje de dominio."""
    try:
        return model_class.objects.get(id=object_id)
    except model_class.DoesNotExist as exc:
        raise ValueError(error_message) from exc
