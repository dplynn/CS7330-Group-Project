import DBInteract

def testing(connection):
    # test fetch user function
    user = DBInteract.fetch_user(connection, "wirskye", "tiktok")
    print("\nTesting fetch_user:")
    if user is None:
        print("User not found")
    else:
        print(user)

    user = DBInteract.fetch_user(connection, "kwirskye", "tiktok")
    print("\nTesting fetch_user:")
    if user is None:
        print("User not found")
    else:
        print(user)

    
    # test fetch posts from a social media function
    posts = DBInteract.fetch_posts_socialmedia(connection, "poopchat")
    print("\nTesting fetch_posts_socialmedia:")
    if len(posts) == 0:
        print("Posts from social media not found")
    else:
        for post in posts:
            print(post)

    posts2 = DBInteract.fetch_posts_socialmedia(connection, "facebook")
    print("\nTesting fetch_posts_socialmedia:")
    if len(posts2) == 0:
        print("Posts from social media not found")
    else:
        for post in posts2:
            print(post)

    # test fetch posts within a time frame function
    posts3 = DBInteract.fetch_posts_betweentime(connection, "10/5/2023 11:00", "10/6/2023 11:00")
    print("\nTesting fetch_posts_between time:")
    if len(posts3) == 0:
        print("Posts from time range not found")
    else:
        for post in posts3:
            print(post)

    posts4 = DBInteract.fetch_posts_betweentime(connection, "10/5/2025 11:00", "10/6/2025 11:00")
    print("\nTesting fetch_posts_between time:")
    if len(posts4) == 0:
        print("Posts from time range not found")
    else:
        for post in posts4:
            print(post)

    # test fetch posts from a username and media function
    posts5 = DBInteract.fetch_posts_user(connection, "kwirskye", "facebook")
    print("\nTesting fetch_posts_user:")
    if len(posts5) == 0:
        print("Posts from user/social media combo not found")
    else:
        for post in posts5:
            print(post)

    posts6 = DBInteract.fetch_posts_user(connection, "wirskye", "facebook")
    print("\nTesting fetch_posts_user:")
    if len(posts6) == 0:
        print("Posts from user/social media combo not found")
    else:
        for post in posts6:
            print(post)

    
    # test posts from a first name/last name function
    posts7 = DBInteract.fetch_posts_twonames(connection, "Katherine", "Wirskye")
    print("\nTesting fetch_posts_twonames:")
    if len(posts7) == 0:
        print("Posts from first name/last name combo not found")
    else:
        for post in posts7:
            print(post)
    print(len(posts7))

    posts8 = DBInteract.fetch_posts_twonames(connection, "Lucas", "Wirskye")
    print("\nTesting fetch_posts_twonames:")
    if len(posts8) == 0:
        print("Posts from first name/last name combo not found")
    else:
        for post in posts8:
            print(post)

    # test querying experiment
    experiment_posts, experiment_fields = DBInteract.fetch_posts_experiment(connection, "proj3")
    print("\nTesting fetch_posts_experiement:")
    if len(experiment_posts) == 0:
        print("No posts from experiement found")
    else:
        for post in experiment_posts:
            print(post)
        for field in experiment_fields:
            print(field)

    experiment_posts2, experiment_fields2 = DBInteract.fetch_posts_experiment(connection, "goofyproj")
    print("\nTesting fetch_posts_experiement:")
    if len(experiment_posts2) == 0:
        print("No posts from experiement found")
    else:
        for post in experiment_posts2:
            print(post)
        for field in experiment_fields2:
            print(field)