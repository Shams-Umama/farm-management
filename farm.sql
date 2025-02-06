
create database farmer;
use farmer;

create table user(
    'id 'int(11) primary key auto_increment,
    'username' varchar(35),
    'email' varchar(30),
   ' password 'varchar(500)
);

insert into user('id','username','email','password')values
('7','radhika', 'radhika@gmail.com','scrypt:32768:8:1$zUjgPwDz4to57ns9$13fa3862d27e19f8b046f6ad7568f4f1f4b836bb916706234cd1b980debbc297a08f870cb6f4ff9fc6485cc10ae1f9791d6ff90efe0c09bb68f14abca4aa7371');

create table 'register'(
    'rid' int(11) primary key auto_increment,
    'farmername' varchar(50),
    'adharnumber' int (12),
    'age' int (100),
    'gender' varchar (50),
    'phonenumber' int(12),
    address varchar(100),
    'farmingtype' varchar(50)
);



insert into 'register' ('rid','farmnername','adharnumber','age','gender','phonenumber','address','farmingtype') values
('2','Raja','2147483647','25','male','2147483647','banglore','paddy');

create table 'farming' (
    'fid' int primary key auto_increment,
    'farmingtype' varchar (100)
    );

    insert into 'farming'('fid','farmingtype') values
    ('1','Silk'),
	('2','Coconut')
    ('3','Paddy');


    create table 'products'(
        'pid' int (11)primary key auto_increment,
        'productname' varchar(50),
        'productdesc' varchar(50),
        'price' int(100),
        'username' varchar(50),
        'email' varchar(50)
    );

    insert into 'products'('pid','productname','productdesc','price','username','email') values
    ('4','Coconut','Coconuts are tropical fruits from the coconut palm','250','radhika','radhika@gmail.com'),
    ('5','seedlling','A seedling is a young plant that has just emerged' ,'200','radhika','radhika@gmail.com' );


alter table `products` 
add primary key (`pid`);

alter table `farming` 
add primary key (`fid`);

alter table`register`
add primary key(`rid`);

alter table 'user'
add primary key ('id');

commit;


