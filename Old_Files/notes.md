Questions for Professor:

- How does the post data initially get into the database? Is it initially populated with just posts and users? Can it be initially populated with projects and project data too?
- “I will publish a rubric to give you a sense of how I will evaluate your work.”
    - When is demo rubric available?
- “Querying post. Your system should allow (at least) the following criteria (or a combination of both (by AND only))”
    - What does by and only mean?
- “In addition, for the post itself, we will like to store the time it was posted (year/month/day/hour/minute, second may or may not be available).”
    - Do we ignore the second field entirely? Or make it optional? If it is optional, how do we compare between posts with seconds and posts without seconds?
- If a post is associated with a project, does that automatically mean it’s being analyzed for all the fields associated with the project? Or is it only being analyzed for fields the user explicitly enters data for?
- Do all projects have the same fields?

Notes for Team:

Preferred demo date?
- Davis -> Monday

I believe we should still be able to add users and posts with some null fields (looks like some of this is NOT NULL right now)
“There are other information about a post that may or may not be available, and if they are, we need to record them: location of the post (city, state, country), number of likes and dislikes (as non-negative integers) and whether the post contains multimedia component (e.g. video, audio – there is no need to distinguish among them).”
“For each poster, we would like to store the following information (if available): first name and last name of the poster, country of birth, country of residence; age; gender; whether the user is an “verified” user at that media.”
- Davis -> Agree, will change INIT and Insert Functions. 

The datetime formatting between the different csv files (project data and post data data) is inconsistent — it should probably be formatted the same way whenever we have it in string form
Can our code handle post text that has a comma in it? (I notice there’s one post with a comma in it and it’s the only one with quotation marks around the text—should they all have quotation marks to be safe?)
- Davis -> I will standardize the post and project data. I'll look into the comma question. 

Do we want to be able to store all the fields associated with a project? This would likely be necessary if, after clarifying with prof, he says that each post in a project needs to be analyzed for every field in that project

Right now, the insert_projectdata function wouldn’t allow us to analyze a post for multiple fields associated with the same project. I think we night need to rethink how we input the project data. According to the rubric, it seems like we first need to be able to insert a list of all the posts associated with a project and then separately input field results for each post:
“Enter the set of posts that is associated with a project. Notice that if a post already exists, it should not be stored in the database multiple times.”
“For a project, entering the analysis result (notice that the system should allow partial results to be entered).”
(Relating to the previous two points) Assuming that each post associated with a project does indeed need to be analyzed for all fields associated with that project, then I suggest we implement it like this:
1) for each project, we need to store a list of all the applicable fields
2) the program user can enter a list of posts associated with the project, and then the project data table will be populated with tuples for each combination of post and field name (so like if the project has 5 posts, and 3 fields, there would be 15 tuples)
3) the program user can enter the results for a field for a post (anything they don’t enter data for will remain null)