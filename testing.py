import DBInteract
from datetime import datetime

def test_fetch_functions(connection):

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

    # testing fetch post

    post = DBInteract.fetch_post(connection, "dlynn", "twitter" , datetime.strptime("2023-10-9 20:00:00", "%Y-%m-%d %H:%M:%S"))
    print("\nTesting fetch_post:")
    if post is None:
        print("Post not found")
    else:
        print(post)
    
    post = DBInteract.fetch_post(connection, "dplynn", "twitter" , datetime.strptime("2023-10-9 20:00:00", "%Y-%m-%d %H:%M:%S"))
    print("\nTesting fetch_post:")
    if post is None:
        print("Post not found")
    else:
        print(post)
    
    # test fetch_project
    
    project = DBInteract.fetch_project(connection, "proj100")
    print("\nTesting fetch_project:")
    if project is None:
        print("Project not found")
    else:
        print(project)

    project = DBInteract.fetch_project(connection, "proj1")
    print("\nTesting fetch_project:")
    if project is None:
        print("Project not found")
    else:
        print(project)

    # test fetch project data
        
    proj_data = DBInteract.fetch_projectdata(connection, "proj99999","dplynn","twitter",datetime.strptime("2023-10-9 20:00:00", "%Y-%m-%d %H:%M:%S"),"field9")
    print("\nTesting fetch_projectdata:")
    if proj_data is None:
        print("Project data not found")
    else:
        print(proj_data)
    
    proj_data = DBInteract.fetch_projectdata(connection, "proj9","dplynn","twitter",datetime.strptime("2023-10-9 20:00:00", "%Y-%m-%d %H:%M:%S"),"field9")
    print("\nTesting fetch_projectdata:")
    if proj_data is None:
        print("Project data not found")
    else:
        print(proj_data)

def test_individual_queries(connection):
    
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
    posts4 = DBInteract.fetch_posts_betweentime(connection, "10/5/2025 11:00", "10/6/2025 11:00")
    print("\nTesting fetch_posts_between time:")
    if len(posts4) == 0:
        print("Posts from time range not found")
    else:
        for post in posts4:
            print(post)
    
    posts3 = DBInteract.fetch_posts_betweentime(connection, "10/5/2023 11:00", "10/6/2023 11:00")
    print("\nTesting fetch_posts_between time:")
    if len(posts3) == 0:
        print("Posts from time range not found")
    else:
        for post in posts3:
            print(post)

    # test fetch posts from a username and media function
    posts6 = DBInteract.fetch_posts_user(connection, "wirskye", "facebook")
    print("\nTesting fetch_posts_user:")
    if len(posts6) == 0:
        print("Posts from user/social media combo not found")
    else:
        for post in posts6:
            print(post)

    posts5 = DBInteract.fetch_posts_user(connection, "kwirskye", "facebook")
    print("\nTesting fetch_posts_user:")
    if len(posts5) == 0:
        print("Posts from user/social media combo not found")
    else:
        for post in posts5:
            print(post)
    
    # test posts from a first name/last name function
    posts8 = DBInteract.fetch_posts_twonames(connection, "Lucas", "Wirskye")
    print("\nTesting fetch_posts_twonames:")
    if len(posts8) == 0:
        print("Posts from first name/last name combo not found")
    else:
        for post in posts8:
            print(post)
   
    posts7 = DBInteract.fetch_posts_twonames(connection, "Katherine", "Wirskye")
    print("\nTesting fetch_posts_twonames:")
    if len(posts7) == 0:
        print("Posts from first name/last name combo not found")
    else:
        for post in posts7:
            print(post)
    print(len(posts7))

def test_querying_experiment(connection):
    # test querying experiment
    experiment_posts, experiment_fields = DBInteract.fetch_posts_experiment(connection, "proj3")
    print("\nTesting fetch_posts_experiment:")
    if len(experiment_posts) == 0:
        print("No posts from experiment found")
    else:
        for post in experiment_posts:
            print(post)
        for field in experiment_fields:
            print(field)

    experiment_posts2, experiment_fields2 = DBInteract.fetch_posts_experiment(connection, "goofyproj")
    print("\nTesting fetch_posts_experiment:")
    if len(experiment_posts2) == 0:
        print("No posts from experiment found")
    else:
        for post in experiment_posts2:
            print(post)
        for field in experiment_fields2:
            print(field)

def test_all4_query(connection):

    print("\n1) Testing all 4 query (only social media)")
    result = DBInteract.fetch_posts_all4(connection, "facebook",None,None,None,None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n2) Testing all 4 query (only time period)")
    result = DBInteract.fetch_posts_all4(connection, None, datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),None,None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n3) Testing all 4 query (only username of a social media)")
    result = DBInteract.fetch_posts_all4(connection, None, None,None,"dplynn",None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n4) Testing all 4 query (only first/last name)")
    result = DBInteract.fetch_posts_all4(connection, None, None,None,None,"Katherine","Wirskye")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n5) Testing all 4 query (social media & time period)")
    result = DBInteract.fetch_posts_all4(connection, "twitter", datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),None,None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n6)Testing all 4 query (social media & username of social media)")
    result = DBInteract.fetch_posts_all4(connection, "tiktok", None,None,"dplynn",None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n7)Testing all 4 query (social media & first/last name)")
    result = DBInteract.fetch_posts_all4(connection, "tiktok", None,None,None,"Davis","Lynn")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n8)Testing all 4 query (time period & username of social media)")
    result = DBInteract.fetch_posts_all4(connection, None, datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),"kwirskye",None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n9)Testing all 4 query (time period & first/last name)")
    result = DBInteract.fetch_posts_all4(connection, None, datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),None,"Katherine","Wirskye")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n10)Testing all 4 query (username & first/last name)")
    result = DBInteract.fetch_posts_all4(connection, None, None,None,"BADUSERNAME","Katherine","Wirskye")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n11)Testing all 4 query (social media & time period & username)")
    result = DBInteract.fetch_posts_all4(connection, "tiktok", datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),"kwirskye",None,None)
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n12) Testing all 4 query (social media & time period & first/last name)")
    result = DBInteract.fetch_posts_all4(connection, "tiktok", datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),None,"Bonita","Davis")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n13)Testing all 4 query (social media & username & first/last name)")
    result = DBInteract.fetch_posts_all4(connection, "tiktok", None,None,"bdavis","Bonita","Davis")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n14) Testing all 4 query (time period & username & first/last name)")
    result = DBInteract.fetch_posts_all4(connection, None, datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),"bdavis","Bonita","Davis")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")

    print("\n15) Testing all 4 query (ALL FOUR FIELDS)")
    result = DBInteract.fetch_posts_all4(connection, "tiktok", datetime.strptime("2023-11-1 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.strptime("2023-11-5 00:00:00", "%Y-%m-%d %H:%M:%S"),"bdavis","Bonita","Davis")
    if len(result) == 0:
        print("No posts found")
    else:
        print(str(len(result))+" posts found")


def testing(connection):

    #test_fetch_functions(connection)

    #test_individual_queries(connection)

    #test_querying_experiment(connection)

    test_all4_query(connection)