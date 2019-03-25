def get_user_id_by_name_and_server_id(client, user_name, server):
    for user in server.members:
        if user_name == str(user):
            return user.id

    return None