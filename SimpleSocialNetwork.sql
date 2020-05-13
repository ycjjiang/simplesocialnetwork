-- This file contains the deliverables for items 2 and 3 of the project.

-- Part 2.
drop database if exists SimpleSocialNetwork;
create database SimpleSocialNetwork;
use SimpleSocialNetwork;

-- sexInfo
-- contains info about user's sex
drop table if exists sexInfo;
create table sexInfo (
    sexID int not null auto_increment,
    sex varchar(10) check (sex in ('Male', 'Female', 'Other')),
    primary key (sexID)
);

-- vocationInfo
-- contains info about user's vocation preferences
drop table if exists vocationInfo;
create table vocationInfo (
    vocationID int not null auto_increment,
    vocation varchar(50),
    primary key (vocationID)
);

-- religionInfo
-- contains info about user's religion preferences
drop table if exists religionInfo;
create table religionInfo (
    religionID int not null auto_increment,
    religion varchar(50),
    primary key (religionID)
);

-- userInfo
-- contains all relevant user info
drop table if exists userInfo;
create table userInfo (
    userID int not null auto_increment,
    userName varchar(50) not null unique,
    firstName varchar(50),
    middleName varchar(50),
    lastName varchar(50),
    birthdate date,
    sexID int,
    vocationID int,
    religionID int,
    primary key (userID, userName),
    foreign key (sexID) references sexInfo(sexID) on delete cascade,
    foreign key (vocationID) references vocationInfo(vocationID) on delete cascade,
    foreign key (religionID) references religionInfo(religionID) on delete cascade
);

-- follower
-- contains info about who follows who. userID column follows followerID column
drop table if exists follower;
create table follower (
    userID int not null,
    followerID int not null,
    primary key (userID, followerID),
    foreign key (userID) references userInfo(userID) on delete cascade,
    foreign key (followerID) references userInfo(userID) on delete cascade
);

-- groupInfo
-- contains info about groups such as name and number of members
drop table if exists groupInfo;
create table groupInfo (
    groupID int not null auto_increment,
    groupName varchar(50),
    numMembers int,
    primary key (groupID)
);

-- gMember
-- contains info about which user is in which group
drop table if exists gMember;
create table gMember (
    userID int,
    groupID int,
    primary key (userID, groupID),
    foreign key (userID) references userInfo(userID) on delete cascade,
    foreign key (groupID) references groupInfo(groupID) on delete cascade
);

-- postInfo
-- contains all post (or response) content info, including reactions
drop table if exists postInfo;
create table postInfo (
    postID int not null auto_increment,
    userID int,
    createdOn datetime default current_timestamp,
    content varchar(5000),
    numLikes int default 0,
    numDislikes int default 0,
    primary key (postID),
    foreign key (userID) references userInfo(userID) on delete cascade
);

-- reactionInfo
-- contains the possible reactions a user can give to a post (like/dislike)
drop table if exists reactionInfo;
create table reactionInfo (
    reactionID int not null auto_increment,
    reaction varchar(50) not null,
    primary key (reactionID)
);

-- reaction
-- contains posts that have been reacted to and who reacted to them and what their reaction was
drop table if exists reaction;
create table reaction (
    userID int,
    postID int,
    reactionID int,
    primary key (userID, postID),
    foreign key (userID) references userInfo(userID) on delete cascade,
    foreign key (postID) references postInfo(postID) on delete cascade,
    foreign key (reactionID) references reactionInfo(reactionID) on delete cascade
);

-- postRead
-- contains info about if a post is read by a user 
drop table if exists postRead;
create table postRead (
    userID int,
    postID int,
    primary key (userID, postID),
    foreign key (userID) references userInfo(userID) on delete cascade,
    foreign key (postID) references postInfo(postID) on delete cascade
);

-- response
-- contains info about which post has been responded to and what the response was
drop table if exists response;
create table response (
    responseID int,
    postID int,
    primary key (responseID, postID),
    foreign key (responseID) references postInfo(postID) on delete cascade,
    foreign key (postID) references postInfo(postID) on delete cascade    
);

-- linkInfo
-- this table holds link information related to posts
drop table if exists linkInfo;
create table linkInfo (
    postID int,
    link varchar(500) not null,
    primary key (postID, link),
    foreign key (postID) references postInfo(postID) on delete cascade
);

-- imageInfo
-- this table holds image info related to posts
drop table if exists imageInfo;
create table imageInfo (
    postID int,
    image varchar(500) not null,
    primary key (postID, image),
    foreign key (postID) references postInfo(postID) on delete cascade
);

-- topicInfo
-- this table contains all topics
drop table if exists topicInfo;
create table topicInfo (
    topicID int not null auto_increment,
    topicName varchar(50) not null,
    primary key (topicID)
);

-- follows
-- contains users and their followed topics
drop table if exists follows;
create table follows (
    userID int,
    topicID int,
    primary key (userID, topicID),
    foreign key (userID) references userInfo(userID) on delete cascade,
    foreign key (topicID) references topicInfo(topicID) on delete cascade
);

-- subtopic
-- tells you which topics are subtopics of other topics
drop table if exists subtopic;
create table subtopic (
    subtopicID int not null,
    topicID int,
    primary key (subtopicID, topicID),
    foreign key (subtopicID) references topicInfo(topicID) on delete cascade,
    foreign key (topicID) references topicInfo(topicID) on delete cascade
);

-- topic
-- tells you the topic of a post
drop table if exists topic;
create table topic (
    postID int,
    topicID int,
    primary key (postID, topicID),
    foreign key (postID) references postInfo(postID) on delete cascade,
    foreign key (topicID) references topicInfo(topicID) on delete cascade
);


-- Part 3.
-- I was unable to find a specific dataset that could populate my entire database with non-trivial data. 
-- As per question @199 on Piazza, below are some random generated data I created to initially populate this database with. 
-- More info will populated in the demo video

insert into sexInfo (sex) values
    ('Male'),
    ('Female'),
    ('Other');
    
insert into vocationInfo (vocation) values
    ('Doctor'),
    ('Priest'),
    ('Pharmacist'),
    ('Engineer'),
    ('Singer'),
    ('Dancer'),
    ('Actor');
    
insert into religionInfo (religion) values
    ('Hinduism'),
    ('Buddhism'),
    ('Islam'),
    ('Confucianism'),
    ('Christianity'),
    ('Taoism'),
    ('Judaism'),
    ('Atheism');
    
insert into userInfo (userName, firstName, middleName, lastName, birthdate, sexID, vocationID, religionID) values
    ('ycjasper', 'Jasper', 'Yucheng', 'Jiang', '1998-05-23', 1, 4, 8),
    ('sxqn', 'Sherry', 'Xiran', 'Qian', '1998-08-26', 2, 4, 8),
    ('davidchoi12', 'David', 'Sunghoon', 'Choi', '1998-05-12', 1, 1, 5),
    ('samanthahuang98', 'Samantha', '', 'Huang', '1998-03-14', 2, 4, 4),
    ('jklee98', 'Kevin', 'Jaewuk', 'Lee', '1998-07-21', 1, 3, 2),
    ('_taeyang_', 'YoungBae', 'Taeyang', 'Dong', '1994-05-18', 1, 5, 5),
    ('raemondo', 'Raymond', '', 'Lu', '1998-07-12', 1, 1, 8),
    ('linglu', 'Ling', '', 'Lu', '1998-03-19', 2, 4, 8),
    ('ellenlau', 'Ellen', '', 'Lau', '1998-02-03', 2, 4, 8);
    
insert into follower (userID, followerID) values
    (1,2), (1,3), (1,4), (1,5), (2,1), (2,3), (2,4), (2,5), (3,1), (3,2), (3,5), (4,1), (4,2), (5,1), (5,2), (5,3), (8,2), (8,7), (9,2);
    
insert into groupInfo (groupName, numMembers) values
    ('Summoners War', 3),
    ('third row', 2),
    ('basketball club', 3),
    ('pubg', 3),
    ('uvhs', 3),
    ('kpop', 7);

insert into gMember (userID, groupID) values
    (1,1), (1,3), (1,6), (2,2), (2,5), (3,1), (3,3), (3,4), (3,6), (4,2), (5,1), (5,4), (5,6), (6,6), (7,3), (7,4), (8,5), (8,6), (9,5), (9,6);

insert into postInfo (userID, createdOn, content) values
    (1, '2020-03-21 14:34:12', 'I cant believe uw is cancelling all in-person activity!!'),
    (2, '2020-03-22 12:34:27', 'I know right?! Academic mission failed.'),
    (6, '2020-03-27 20:12:23', 'Dope dance..... congratz!'),
    (3, '2020-03-27 21:01:01', 'Who wants to play some ball???'),
    (1, '2020-03-27 21:02:23', 'im down! meet at park?'),
    (7, '2020-03-27 21:02:47', 'c u guys there!!'),
    (8, '2020-03-30 08:23:12', 'What do you guys think about this design??'),
    (9, '2020-03-30 09:12:12', 'wow thats amazing!!'),
    (2, '2020-03-31 09:23:23', 'cool stuff!! check mine out too!!');
    
insert into reactionInfo (reaction) values
    ('like'), ('dislike');

insert into response (responseID, postID) values
    (2,1), (5,4), (6,4), (8,7), (9,7);

insert into topicInfo (topicName) values
    ('Games'), ('RPG'), ('Design'), ('Industrial Design'), ('Sports'), ('Basketball'), ('News');
    
insert into follows (userID, topicID) values
    (1,2), (1,6), (2,4), (3,2), (3,6), (4,3), (5,2), (6,6), (7,1), (7,2), (7,6), (8,3), (8,4), (9,3), (9,4);
    
insert into subtopic (subtopicID, topicID) values
    (2,1), (4,3), (6,5);

insert into topic (postID, topicID) values
    (1,7), (2,7), (3,1), (4,5), (5,5), (6,5), (7,4), (8,4), (9,4);