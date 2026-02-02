# -----  CREATE DATABASE -----
create database bank_db;
use bank_db; 

#----- Accounts table -----
create table accounts(
acc_no bigint primary key,
name varchar(100) not null, 
balance int default 500);

# ----- Transactions table -----
create table transactions(
id int auto_increment primary key,
acc_no bigint,
type varchar(60),
amount float,
foreign key(acc_no) references accounts(acc_no));

# ----- View data -----
select * from accounts;
select * from transactions;

# ----- Added later for PIN-based authentication -----
alter table accounts add column PIN int not null;
