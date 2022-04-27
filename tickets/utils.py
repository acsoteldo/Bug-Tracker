def is_admin(user):
    if user.groups.filter(name="admin").exists() or user.is_superuser:
        return True
    else:
        return False
