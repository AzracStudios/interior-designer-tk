
TABLES = {}

TABLES['users'] = """
create table users (
  uid varchar(36) not null,
  name varchar(255) not null,
  email varchar(255) not null unique,
  password varchar(255) not null,
  primary key (uid)
)
"""

TABLES["feedback"] = """
create table feedback (
  uid varchar(36) not null,
  userId varchar(36),
  constraint FK_userIdFeedback foreign key (userId) references users(uid),
  primary key (uid)
)
"""

TABLES["inquiries"] = """
create table inquiries (
  uid varchar(36) not null,
  userId varchar(36),
  designs varchar(4096) not null,
  constraint FK_userIdInquiry foreign key (userId) references users(uid),
)
"""

TABLES['styles'] = """
create table styles (
  uid varchar(36) not null,
  style_name varchar(255) not null unique,
  style_banner varchar(255) not null,
  primary key (uid)
)
"""

TABLES['rooms'] = """
create table rooms (
  uid varchar(36) not null,
  room_name varchar(255) not null unique,
  room_banner varchar(255) not null,
  room_card varchar(255) not null,
  primary key (uid)
)
"""

TABLES["designs"] = """
create table designs (
  uid varchar(36) not null,
  design_name varchar(255) not null unique,
  design_img varchar(255) not null unique,
  roomId varchar(36) not null,
  styleId varchar(36) not null,
  constraint FK_roomId foreign key (roomId) references rooms(uid),
  constraint FK_styleId foreign key (styleId) references styles(uid),
  primary key (uid)
)
"""

TABLES["likes"] = """
create table likes (
  uid varchar(36) not null,
  userId varchar(36) not null,
  designId varchar(36) not null,
  constraint FK_userId foreign key (userId) references users(uid),
  constraint FK_designId foreign key (designId) references designs(uid)
)
"""
