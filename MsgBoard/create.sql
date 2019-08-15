create table msg(
     id int primary key auto_increment,
     name  varchar(20) not null default "",
     email varchar(50) not null default "",
     address varchar(100) not null default "",
     msg varchar(200) not null default ""
) engine=innodb character set utf8;