# This is the simple social-network client, it runs on the command line interface.
# This file contains the deliverables for item 4 of the project
# reference used for python cmd module: https://docs.python.org/3/library/cmd.html

import cmd
import pandas
import mysql.connector

class cli:
    # the following functions define all required mySQL connections and commands
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "localhost",
            database = "SimpleSocialNetwork",
            user = "test"
            # password = ""
        )
        self.cursor = self.connection.cursor()
    
    def query(self, query, vals = None):
        self.cursor.execute(query, vals)
        return self.cursor
    
    def commit(self):
        self.connection.commit()
    
    def rollback(self):
        self.connection.rollback()
    
class SimpleSocialNetwork(cmd.Cmd):
    intro = 'Welcome to InstaBook, the BEST social networking tool! Type help or ? to list commands.'
    prompt = '<InstaBook> '
    
    # initializes the db connection and sets userID to None, as nobody is 'logged in' yet
    def __init__(self):
        super(SimpleSocialNetwork, self).__init__()
        self.mySQL_cli = cli()
        self.this_userID = None
    
    # Part 4. (a) 
    # creates a post by asking the user for a topic and its content (the post). 
    # If the topic exists, the post will be created and topic table is updated accordingly.
    # If the topic does not exist, it will be created as a new topic and the post will be created under that topic.
    # topicInfo, postInfo, and topic tables are updated accordingly
    def do_createpost(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            topic = input("Please enter your post topic: ")
            content = input("Please enter your post : ")
            
            if not topic or not content:
                print("Missing input. Unable to create post.")

            try:
                if topic and content:
                    topicID = None
                    findTopic = "select topicID from topicInfo where topicName = '{}';".format(topic)
                    result = self.mySQL_cli.query(findTopic).fetchall()
                    if result:
                        topicID = result[0][0]
                    else:
                        createTopic = "insert into topicInfo values (%s, %s);"
                        vals = (topicID, topic)
                        topicID = self.mySQL_cli.query(createTopic, vals).lastrowid
                        print("Created new topic {}. It is topic number {}.".format(topic, topicID))

                    if topicID:
                        createPost = "insert into postInfo (userID, content) values (%s, %s);"
                        vals = (self.this_userID, content)
                        postID = self.mySQL_cli.query(createPost, vals).lastrowid
                        print("Post created under topic {}.".format(topic))

                        if postID:
                            createTopicPost = "insert into topic values (%s, %s);"
                            vals = [postID, topicID]
                            self.mySQL_cli.query(createTopicPost, vals).lastrowid
                            self.mySQL_cli.commit()

            except mysql.connector.Error as error :
                print("Unable to create post. Error: {}. Please try again.".format(error))
                self.mySQL_cli.rollback()

    # Part 4. (b) 
    # creates a group by asking the user for a group name and the person they want to invite. 
    # Updates groupInfo and gMember accordingly
    def do_creategroup(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            groupName = input("Please enter your group name: ")
            
            if not groupName:
                print("No input. Unable to create group.")
            
            else:
                getUsers ="select userID, username from userInfo;"
                result = self.mySQL_cli.query(getUsers).fetchall()
                printData = pandas.DataFrame(result, columns=['userID', 'username'])
                print("Here are all currently existing users: \n {}".format(printData))
                invitedID = input("Please enter the userID of who you want to invite to {}: ".format(groupName))

                if not invitedID:
                    print("No input. Unable to create group.")
                    return

                try:
                    createGroup = "insert into groupInfo (groupName, numMembers) values ('{}', 2);".format(groupName)
                    groupID = self.mySQL_cli.query(createGroup).lastrowid
                    updateMembers = "insert into gMember (groupID, userID) values (%s, %s);"
                    vals = [(groupID, self.this_userID), (groupID, int(invitedID))]
                    self.mySQL_cli.cursor.executemany(updateMembers, vals)
                    self.mySQL_cli.commit()
                    print("Group {} created! User {} has joined your group.".format(groupName, invitedID))

                except mysql.connector.Error as error :
                    print("Unable to create group. Error: {}".format(error))
                    self.mySQL_cli.rollback()

    # Part 4. (b) 
    # displays all groups and asks user for the ID of the group they want to follow. 
    # If already following, an error will be thrown. 
    # groupInfo and gMember tables are updated accordingly.
    def do_followgroup(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            getGroups ="select groupID, groupName from groupInfo;"
            result = self.mySQL_cli.query(getGroups).fetchall()
            printData = pandas.DataFrame(result, columns=['groupID', 'groupName'])
            print("Here are all currently existing groups: \n {}".format(printData))
            groupID = input("Please enter the groupID of the group you would like to follow: ")

            if not groupID:
                print("No input. Unable to follow group.")
                return

            try:
                findGroup = "select * from groupInfo where groupID = {}".format(groupID)
                result = self.mySQL_cli.query(findGroup).fetchall()
                join = "update groupInfo set numMembers = numMembers + 1 where groupID = {};".format(groupID)
                self.mySQL_cli.query(join)
                self.mySQL_cli.commit()
                updateMembers = "insert into gMember (groupID, userID) values (%s, %s);"
                vals = (groupID, self.this_userID)
                self.mySQL_cli.query(updateMembers, vals)
                self.mySQL_cli.commit()
                print("You are now following group {}.".format(groupID))

            except mysql.connector.Error as error :
                print("Unable to follow group {}. Error: {}".format(groupID, error))
                self.mySQL_cli.rollback()

    # Part 4. (c) 
    # displays all topics and asks user for the ID of the topic they want to follow. 
    # If already following, an error will be thrown. 
    # topicInfo and follows tables are updated accordingly.
    def do_followtopic(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            getTopics ="select topicID, topicName from topicInfo;"
            result = self.mySQL_cli.query(getTopics).fetchall()
            printData = pandas.DataFrame(result, columns=['topicID', 'topicName'])
            print("Here are all currently existing topics: \n {}".format(printData))
            topicID = input("Please enter the topicID of the topic you would like to follow: ")

            if not topicID:
                print("No input. Unable to follow topic.")
                return

            try:
                findTopic = "select * from topicInfo where topicID = {};".format(topicID)
                result = self.mySQL_cli.query(findTopic).fetchall()
                followTopic = "insert into follows values (%s, %s);"
                vals = (self.this_userID, topicID)
                self.mySQL_cli.query(followTopic, vals)
                self.mySQL_cli.commit()
                print("You are now following topic {}.".format(topicID))

            except mysql.connector.Error as error :
                print("Topic not found. Unable to follow topic {}. Error: {}".format(topicID, error))
                self.mySQL_cli.rollback()
                
    # Part 4. (d)
    # displays all posts posted by current user
    def do_getmyposts(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            try:
                get_my_posts_query = "select * from postInfo where userID = {};".format(self.this_userID)
                result = self.mySQL_cli.query(get_my_posts_query).fetchall()
                
                if not result:
                    print("You have no posts.")
                    
                else:
                    print("Here are your posts.")
                    printData = pandas.DataFrame(result, columns=['postID', 'userID', 'createdOn', 'content', 'numLikes', 'numDislikes'])
                    print(printData)
                    
            except mysql.connector.Error as error :
                print("Unable to retreive your posts. Error: {}".format(error))
                self.mySQL_cli.rollback() 
        
    # Part 4. (d) 
    # displays all posts followed by current user
    def do_getallposts(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            try:
                getPosts = '''
                    select postID, userID, topicName, createdOn, content, numLikes, numDislikes
                    from postInfo
                    inner join topic using (postID)
                    inner join topicInfo using (topicID)
                    where (
                        topicID in
                            (select topicID from follows where userID = {} ) or
                        userID IN
                            (select userID from follower where followerID = {} ));
                '''.format(self.this_userID, self.this_userID)
                result = self.mySQL_cli.query(getPosts).fetchall()

                if not result:
                    print("You are following no posts.")
                    
                else:
                    print("Here are your followed posts.")
                    printData = pandas.DataFrame(result, columns=['postID', 'userID', 'topicName', 'createdOn', 'content', 'numLikes', 'numDislikes'])
                    print(printData)

            except mysql.connector.Error as error :
                print("Unable to retreive all posts. Error: {}".format(error))
                self.mySQL_cli.rollback()

    # Part 4. (d) 
    # display all new posts the current user is following (both followed topics and posts by followed users). 
    # postRead table is updated accordingly so the same posts should never appear twice for the same user when using this feature
    def do_getnewposts(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
        else:
            try:
                getPosts = '''
                    select postID, userID, topicName, createdOn, content, numLikes, numDislikes
                    from postInfo
                    inner join topic using (postID)
                    inner join topicInfo using (topicID)
                    where (
                        topicID in
                            (select topicID from follows where userID = {} ) or
                        userID IN
                            (select userID from follower where followerID = {} ))
                    and (postID not in
                            (select postID from postRead where userID = {} ));
                '''.format(self.this_userID, self.this_userID, self.this_userID)
                result = self.mySQL_cli.query(getPosts).fetchall()

                if not result:
                    print("You have no new posts.")
                    
                else:
                    print("Here are your new posts.")
                    printData = pandas.DataFrame(result, columns=['postID', 'userID', 'topicName', 'createdOn', 'content', 'numLikes', 'numDislikes'])
                    print(printData)
                    updatepostRead = "insert into postRead values (%s, %s);"
                    vals = [(self.this_userID, postRead[0]) for postRead in result]

                    self.mySQL_cli.cursor.executemany(updatepostRead, vals)
                    self.mySQL_cli.commit()
                    
            except mysql.connector.Error as error :
                print("Unable to get new posts. Error: {}".format(error))
                self.mySQL_cli.rollback()        

    # Part 4. (e) 
    # displays all currently existing posts and asks user for the ID of the post they would like to react to. 
    # asks user if they want to like or dislike. 
    # updates postInfo and reaction tables accordingly.
    def do_reacttopost(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
        else:
            getPosts ="select postID, content from postInfo;"
            result = self.mySQL_cli.query(getPosts).fetchall()
            printData = pandas.DataFrame(result, columns=['postID', 'content'])
            print("Here are all currently existing posts: \n {}".format(printData))
            postID = input("Please enter the postID of the post you would like to react to: ")

            if not postID:
                print("No input. Unable to react to post.")

            try:
                findPost = "select * from postInfo where postID = {};".format(postID)
                result = self.mySQL_cli.query(findPost).fetchall()

                if not result:
                    print("Post not found. Unable to react to post {}.".format(postID))
                    
                else:
                    reactionType = input("Would you like to like or dislike post {}? (like/dislike)".format(postID))

                    if reactionType == 'like':
                        likePost = "update postInfo set numLikes = numLikes + 1 where postID = {};".format(postID)
                        self.mySQL_cli.query(likePost)
                        self.mySQL_cli.commit()
                        updateReaction = "insert into reaction values ('{}', '{}', 1);".format(self.this_userID, postID)
                        self.mySQL_cli.query(updateReaction)
                        self.mySQL_cli.commit()
                        print("You have liked post {}.".format(postID))

                    elif reactionType == 'dislike':
                        dislikePost = "update postInfo set numDislikes = numDislikes + 1 where postID = {};".format(postID)
                        self.mySQL_cli.query(dislikePost)
                        self.mySQL_cli.commit()
                        updateReaction = "insert into reaction values ('{}', '{}', 2);".format(self.this_userID, postID)
                        self.mySQL_cli.query(updateReaction)
                        self.mySQL_cli.commit()
                        print("You have disliked post {}.".format(postID))

                    else:
                        print("Incorrect input. Unable to react to post {}.".format(postID))     

            except mysql.connector.Error as error :
                print("Unable to react to post {}. Error: {}".format(postID, error))
                self.mySQL_cli.rollback()

    # Part 4. (e) 
    # displays all currently existing posts and asks user for the ID of the post they would like to respond to.
    # asks user for the response. 
    # updates postInfo and response tables accordingly with the user response.
    def do_respondtopost(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
            
        else:
            getPosts ="select postID, content from postInfo;"
            result = self.mySQL_cli.query(getPosts).fetchall()
            printData = pandas.DataFrame(result, columns=['postID', 'content'])
            print("Here are all currently existing posts: \n {}".format(printData))
            postID = input("Please enter the postID of the post you would like to respond to: ")
            response = input("Please enter your response: ")

            if not (postID and response):
                print("Incorrect input. Unable to respond to post.")

            try:
                findPost = "select * from postInfo where postID = {};".format(postID)
                result = self.mySQL_cli.query(findPost).fetchall()

                if not result:
                    print("Post not found. Unable to respond to post {}.".format(postID))
                    
                else:
                    createResponse = "insert into postInfo (userID, content) values (%s, %s);"
                    vals = (self.this_userID, response)
                    responseID = self.mySQL_cli.query(createResponse, vals).lastrowid
                    responsePost = "insert into response values (%s, %s);"
                    vals = (responseID, postID)
                    self.mySQL_cli.query(responsePost, vals)
                    self.mySQL_cli.commit()
                    print("You have responded to post {}.".format(postID))

            except mysql.connector.Error as error :
                print("Unable to respond to post {}. Error: {}".format(postID, error))
                self.mySQL_cli.rollback()  
                
    # Part 4. (f) 
    # signs up a user. 
    # asks for info and populates userInfo table in database. 
    # automatically assigns an auto-incremented userID. 
    # username is unique so does not accept duplicates.
    def do_signup(self, arg):
        firstname = input("First Name: ")
        middlename = input("Middle Name (if you don't have a middle name, just press enter): ")
        lastname = input("Last Name: ")
        birthdate = input("Birthday (please use format yyyy-mm-dd): ")
        username = input("Please enter your desired username: ")
        signUpQuery = "insert into userInfo (userName, firstName, middleName, lastName, birthdate) values (%s, %s, %s, %s, %s);"
        vals = (username, firstname, middlename, lastname, birthdate)
        userNum = self.mySQL_cli.query(signUpQuery, vals).lastrowid
        self.mySQL_cli.commit()
        print("Thanks for joining InstaBook, {}! You are user number {}.".format(username ,userNum))

    # Part 4. (f) 
    # basic login functionality, checks if logged in first
    # asks for username (case sensitive). 
    # if username exists in database, you will be logged in and sets current userID to yours
    def do_login(self, arg):
        if self.this_userID != None :
            print("You are already logged in.")
            
        else:
            username = input("Please enter your username: ")
            findUser = "select * from userInfo where username = '{}';".format(username)
            user = self.mySQL_cli.query(findUser).fetchall()

            if not user:
                print("Login Failed. User not found.")
                
            else:
                self.this_userID = user[0][0]
                print("Welcome Back, {}!".format(username))

    # Part 4. (f) 
    # logs out current user and sets userID to None
    def do_logout(self, arg):
        if self.this_userID == None :
            print("You are not logged in.")
            
        else:
            print("You have been logged out.")
            self.this_userID = None
                
    # Part 4. (f) 
    # displays all users and asks for the ID of the user they want to follow. 
    # If already following, an error will be thrown. 
    # follower table is updated accordingly
    def do_followuser(self, arg):
        if self.this_userID == None :
            print("Please login or signup first.")
        else:
            getUsers ="select userID, username from userInfo;"
            result = self.mySQL_cli.query(getUsers).fetchall()
            printData = pandas.DataFrame(result, columns=['userID', 'username'])
            print("Here are all currently existing users: \n {}".format(printData))
            followID = input("Please enter the userID of the user you would like to follow: ")
            
            if not followID:
                print("No input. Unable to follow user.")
                return
            
            try:
                findUser = "select * from userInfo where userID = {};".format(followID)
                result = self.mySQL_cli.query(findUser).fetchall()

                if not result:
                    print("User not found. Unable to follow user {}.".format(followID))
                    
                else:
                    followUser = "insert into follower values (%s, %s);"
                    vals = (self.this_userID, followID)

                    self.mySQL_cli.query(followUser, vals)
                    self.mySQL_cli.commit()
                    print("You are now following user number {}.".format(followID))

            except mysql.connector.Error as error :
                print("Unable to follow user {}. Error: {}".format(followID, error))
                self.mySQL_cli.rollback()  

if __name__ == '__main__':
    SimpleSocialNetwork().cmdloop() 