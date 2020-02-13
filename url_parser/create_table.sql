create database news_parser;
use news_parser;
create table url_information(
  url nvarchar(250) primary key,
  title nvarchar(300) not null,
  html_code blob(2500000) not null,
  url_parent nvarchar(250) not null
  );
 
/*
--Очистка таблицы, запрос к таблице
--Для html_code возможен тип nvarchar, однако максимально может хранить 22000 символов
TRUNCATE TABLE url_information;
select * from url_information
  LIMIT 5;
  */