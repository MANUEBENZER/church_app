def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='Admin').exists()

def is_pastor(user):
    return user.is_authenticated and user.groups.filter(name='Pastor').exists()
def is_secretary(user):
    return user.is_authenticated and user.groups.filter(name='Secretary').exists()