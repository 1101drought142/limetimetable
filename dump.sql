BEGIN;
CREATE TABLE clients (
	id INTEGER NOT NULL, 
	client_bitrix_id INTEGER, 
	client_name VARCHAR(255), 
	client_phone VARCHAR(255), 
	client_mail VARCHAR(255), 
	PRIMARY KEY (id)
);
INSERT INTO clients VALUES(1,'','Иван Иванов Иванович 1','8 983 313 70 82','test@mail.ru');
INSERT INTO clients VALUES(2,'','Иван Иванов Иванович 2','8 983 313 70 82','test@mail.ru');
INSERT INTO clients VALUES(3,'','Иван Иванов Иванович 3','8 983 313 70 82','test@mail.ru');
INSERT INTO clients VALUES(4,'','Иван Иванов Иванович 4','8 983 313 70 82','test@mail.ru');
INSERT INTO clients VALUES(5,'','Иван Иванов Иванович 6 4','8 983 313 70 82','test@mail.ru');
INSERT INTO clients VALUES(6,'','test','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(7,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(8,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(9,'','тест','+7 (912) 011-78-14','tugbaev17@mail.ru');
INSERT INTO clients VALUES(10,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(11,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(12,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(13,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(14,1,'Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(15,'','tets','+7 (912) 233-44-34','tugbaev17@mail.ru');
INSERT INTO clients VALUES(16,'','test','+7 (912) 345-55-65','test@mal.ru');
INSERT INTO clients VALUES(17,'','test','+7 (212) 131-23-21','test@mal.ru');
INSERT INTO clients VALUES(18,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(19,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(20,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(21,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(22,'','Иван','+7 (981) 298-39-12','test@mail.ru');
INSERT INTO clients VALUES(23,'','Иван','+7 (981) 298-39-12','test@mail.ru');
CREATE TABLE orders (
	id INTEGER NOT NULL, 
	date DATE, 
	client INTEGER, 
	payed BOOLEAN, 
	starttime INTEGER, 
	endtime INTEGER, 
	cort INTEGER, 
	time_created DATETIME DEFAULT (CURRENT_TIMESTAMP), 
	PRIMARY KEY (id), 
	FOREIGN KEY(client) REFERENCES clients (id), 
	FOREIGN KEY(starttime) REFERENCES time_interval_objects (id), 
	FOREIGN KEY(endtime) REFERENCES time_interval_objects (id), 
	FOREIGN KEY(cort) REFERENCES cort (id)
);
INSERT INTO orders VALUES(3,'2023-12-11',9,0,2,5,1,'2023-12-03 12:57:23');
INSERT INTO orders VALUES(4,'2023-12-04',14,1,1,5,2,'2023-12-03 18:43:46');
INSERT INTO orders VALUES(5,'2023-12-13',15,0,2,5,1,'2023-12-03 18:47:38');
INSERT INTO orders VALUES(6,'2023-12-13',16,0,23,28,2,'2023-12-04 07:17:49');
INSERT INTO orders VALUES(7,'2023-12-07',17,0,22,25,3,'2023-12-04 07:28:21');
INSERT INTO orders VALUES(8,'2023-12-06',18,0,23,28,2,'2023-12-04 07:58:13');
INSERT INTO orders VALUES(9,'2023-12-16',19,0,25,27,4,'2023-12-04 07:58:29');
INSERT INTO orders VALUES(10,'2023-12-20',20,0,16,18,3,'2023-12-04 07:59:50');
INSERT INTO orders VALUES(11,'2023-12-14',21,0,3,5,1,'2023-12-04 08:01:43');
INSERT INTO orders VALUES(12,'2023-12-05',22,0,23,25,1,'2023-12-04 08:11:39');
INSERT INTO orders VALUES(13,'2023-12-06',23,0,3,5,1,'2023-12-04 08:12:52');
CREATE TABLE typical_raspisanie_objects (
	id INTEGER NOT NULL, 
	weekdays VARCHAR(9), 
	starttime INTEGER, 
	endtime INTEGER, 
	description VARCHAR, 
	cort INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(starttime) REFERENCES time_interval_objects (id), 
	FOREIGN KEY(endtime) REFERENCES time_interval_objects (id), 
	FOREIGN KEY(cort) REFERENCES cort (id)
);
INSERT INTO typical_raspisanie_objects VALUES(1,'0,',11,13,'Ильченко/Лиля',1);
INSERT INTO typical_raspisanie_objects VALUES(2,'2,',17,19,'Ильченко/Лиля',1);
INSERT INTO typical_raspisanie_objects VALUES(3,'0,',17,19,'Ильченко/Дамир Муратаев',1);
INSERT INTO typical_raspisanie_objects VALUES(4,'0,',19,22,'Ильченко/Василиса',1);
INSERT INTO typical_raspisanie_objects VALUES(5,'0,',25,27,'Ильченко/Вадим',1);
INSERT INTO typical_raspisanie_objects VALUES(6,'0,',27,29,'Ильченко/Рамис Лотфуллин',1);
INSERT INTO typical_raspisanie_objects VALUES(7,'0,',11,13,'Махмудов/Карина',2);
INSERT INTO typical_raspisanie_objects VALUES(9,'0,',17,20,'Махмудов/Никас и Раф',2);
INSERT INTO typical_raspisanie_objects VALUES(10,'0,',14,17,'Махмудов/Ева',2);
INSERT INTO typical_raspisanie_objects VALUES(11,'0,',7,9,'Арина/Эльвира Куртымова',1);
INSERT INTO typical_raspisanie_objects VALUES(12,'1,',5,7,'Махмудов/Рамиль Ахунзянов',2);
INSERT INTO typical_raspisanie_objects VALUES(13,'1,',13,15,'Махмудов/Катя и Лена',2);
INSERT INTO typical_raspisanie_objects VALUES(14,'1,',15,17,'Махмудов/Арсланов Мурат',2);
INSERT INTO typical_raspisanie_objects VALUES(15,'1,',15,17,'Ильченко/Белла',1);
INSERT INTO typical_raspisanie_objects VALUES(16,'1,',17,20,'Ильченко/Дамир Махмутов',1);
INSERT INTO typical_raspisanie_objects VALUES(17,'1,',20,22,'Ильченко/Амерханова Алёна',1);
INSERT INTO typical_raspisanie_objects VALUES(18,'1,',13,17,'Константин/Гульнара Еленина',3);
INSERT INTO typical_raspisanie_objects VALUES(19,'1,',17,19,'Арина/Эльвира Мингазова',3);
INSERT INTO typical_raspisanie_objects VALUES(20,'1,',23,25,'Арина/Алсу Зарипова',3);
INSERT INTO typical_raspisanie_objects VALUES(21,'1,',25,27,'Арина/Ирина и Сергей',3);
INSERT INTO typical_raspisanie_objects VALUES(22,'1,',27,29,'Арина/Дана',3);
INSERT INTO typical_raspisanie_objects VALUES(23,'2,',5,7,'Арина/Коноба',1);
INSERT INTO typical_raspisanie_objects VALUES(24,'2,',10,12,'Ильченко/Мама Расула',1);
INSERT INTO typical_raspisanie_objects VALUES(25,'2,',12,14,'Ильченко/Артем Лукьянов',1);
INSERT INTO typical_raspisanie_objects VALUES(26,'2,',25,27,'Ильченко/Ольга',1);
INSERT INTO typical_raspisanie_objects VALUES(27,'2,',27,29,'Ильченко/Рамис Лотфуллин',1);
INSERT INTO typical_raspisanie_objects VALUES(28,'2,',7,9,'Махмудов/Арина с мамой',2);
INSERT INTO typical_raspisanie_objects VALUES(29,'2,',13,15,'Махмудов/Карина',2);
INSERT INTO typical_raspisanie_objects VALUES(30,'2,',17,20,'Махмудов/Ева',2);
INSERT INTO typical_raspisanie_objects VALUES(31,'2,',11,13,'Арина/Света',4);
INSERT INTO typical_raspisanie_objects VALUES(32,'2,',13,15,'Арина/Евгения',4);
INSERT INTO typical_raspisanie_objects VALUES(33,'2,',15,17,'Константин/Гульнара',4);
INSERT INTO typical_raspisanie_objects VALUES(34,'3,',5,7,'Арина/Ксения Коноба',1);
INSERT INTO typical_raspisanie_objects VALUES(35,'3,',7,9,'Арина/Эльвира с мужем',1);
INSERT INTO typical_raspisanie_objects VALUES(36,'3,',12,14,'Ильченко/Афина',1);
INSERT INTO typical_raspisanie_objects VALUES(37,'3,',14,17,'Ильченко/Дамир Махмутов',1);
INSERT INTO typical_raspisanie_objects VALUES(38,'3,',17,19,'Ильченко/Белла',1);
INSERT INTO typical_raspisanie_objects VALUES(39,'3,',23,25,'Ильченко/ Катя Стандарт',1);
INSERT INTO typical_raspisanie_objects VALUES(40,'3,',25,27,'Ильченко/Вадим',1);
INSERT INTO typical_raspisanie_objects VALUES(41,'3,',13,17,'Константин/Гульнара',3);
INSERT INTO typical_raspisanie_objects VALUES(42,'3,',9,11,'Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(43,'3,',19,23,'Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(44,'3,',23,25,'Арина/Сергей Назаров',4);
INSERT INTO typical_raspisanie_objects VALUES(45,'3,',25,27,'Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(46,'4,',11,13,'Ильченко/Сылу',1);
INSERT INTO typical_raspisanie_objects VALUES(47,'4,',13,16,'Ильченко/Марсель',1);
INSERT INTO typical_raspisanie_objects VALUES(48,'4,',16,18,'Ильченко/Артем Лукьянов',1);
INSERT INTO typical_raspisanie_objects VALUES(49,'4,',18,21,'Ильченко/Василиса',1);
INSERT INTO typical_raspisanie_objects VALUES(50,'4,',1,3,'Махмудов/Шайнуров Рафаэль',2);
INSERT INTO typical_raspisanie_objects VALUES(51,'4,',3,7,'Махмудов/Самин Артём',2);
INSERT INTO typical_raspisanie_objects VALUES(52,'4,',9,11,'Махмудов/Алиса',2);
INSERT INTO typical_raspisanie_objects VALUES(53,'4,',17,20,'Махмудов/Ева',2);
INSERT INTO typical_raspisanie_objects VALUES(54,'4,',20,22,'Махмудов/Антея',2);
INSERT INTO typical_raspisanie_objects VALUES(55,'4,',9,11,'Мифтахова Арина/Эльвира',4);
INSERT INTO typical_raspisanie_objects VALUES(56,'4,',11,13,'Мифтахова Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(57,'4,',15,17,'Константин/Гульнара',4);
INSERT INTO typical_raspisanie_objects VALUES(58,'4,',19,23,'Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(59,'4,',23,25,'Арина/Алла 89172388005',4);
INSERT INTO typical_raspisanie_objects VALUES(60,'4,',25,27,'Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(61,'5,',13,17,'Константин/Гульнара',4);
INSERT INTO typical_raspisanie_objects VALUES(62,'5,',17,25,'Арина',4);
INSERT INTO typical_raspisanie_objects VALUES(63,'6,',9,11,'Арина/Диана и Яна',4);
INSERT INTO typical_raspisanie_objects VALUES(64,'6,',11,13,'Арина/СвеРег',4);
INSERT INTO typical_raspisanie_objects VALUES(65,'6,',13,15,'Арина/Евгения',4);
INSERT INTO typical_raspisanie_objects VALUES(66,'6,',15,17,'Арина/Юлия',4);
INSERT INTO typical_raspisanie_objects VALUES(67,'6,',17,19,'Арина/Динис',4);
INSERT INTO typical_raspisanie_objects VALUES(68,'6,',19,21,'Арина',4);
CREATE TABLE cort (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO cort VALUES(1,'Корт №1');
INSERT INTO cort VALUES(2,'Корт №2');
INSERT INTO cort VALUES(3,'Корт №3');
INSERT INTO cort VALUES(4,'Корт №4');
CREATE TABLE userlog (
	id INTEGER NOT NULL, 
	user INTEGER, 
	text TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user) REFERENCES users (id)
);
INSERT INTO userlog VALUES(1,1,'Создан новый блок расписания на  с 23-11-2023 08:00 по 23-11-2023 09:00 на корте 1 для клиента 1 с оплатой True');
INSERT INTO userlog VALUES(2,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(3,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(4,1,'Обновлен блок расписания на  с 23-11-2023 08:00 по 23-11-2023 10:30 на корте 1 для клиента 1 с оплатой False');
INSERT INTO userlog VALUES(5,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(6,1,'Создан новый блок расписания на  с 26-11-2023 10:30 по 26-11-2023 11:30 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(7,1,'Создан новый блок расписания на  с 26-11-2023 08:00 по 26-11-2023 09:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(8,1,'Создан новый блок расписания на  с 26-11-2023 09:00 по 26-11-2023 10:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(9,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(10,1,'Создан новый блок расписания на  с 26-11-2023 09:00 по 26-11-2023 10:30 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(11,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(12,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(13,1,'Удален блок расписания с id3');
INSERT INTO userlog VALUES(14,1,'Создан новый блок расписания на  с 26-11-2023 09:00 по 26-11-2023 10:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(15,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(16,1,'Удален блок расписания с id1');
INSERT INTO userlog VALUES(17,1,'Создан новый блок расписания на  с 26-11-2023 11:00 по 26-11-2023 12:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(18,1,'Обновлен блок расписания на  с 26-11-2023 11:00 по 26-11-2023 12:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(19,1,'Удален блок расписания с id1');
INSERT INTO userlog VALUES(20,1,'Обновлен блок расписания на  с 03-12-2023 08:00 по 03-12-2023 09:30 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(21,1,'Обновлен блок расписания на  с 03-12-2023 08:00 по 03-12-2023 09:30 на корте 1 с оплатой False');
INSERT INTO userlog VALUES(22,1,'Обновлен блок расписания на  с 03-12-2023 08:00 по 03-12-2023 09:30 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(23,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(24,1,'Удален блок расписания с id2');
INSERT INTO userlog VALUES(25,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(26,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(27,1,'Создан новый блок расписания на  с 10-12-2023 08:00 по 10-12-2023 09:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(28,1,'Обновлен блок расписания на  с 10-12-2023 08:00 по 10-12-2023 09:00 на корте 1 с оплатой False');
INSERT INTO userlog VALUES(29,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(30,1,'Удален блок расписания с id1');
INSERT INTO userlog VALUES(31,1,'Создан новый блок расписания на  с 03-12-2023 15:00 по 03-12-2023 16:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(32,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(33,1,'Создан новый блок расписания на  с 03-12-2023 17:00 по 03-12-2023 18:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(34,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(35,1,'Создан новый блок расписания на  с 03-12-2023 15:00 по 03-12-2023 16:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(36,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(37,1,'Обновлен блок расписания на  с 08-12-2023 12:00 по 08-12-2023 13:00 на корте 1 с оплатой False');
INSERT INTO userlog VALUES(38,1,'Создан новый блок расписания на  с 08-12-2023 09:30 по 08-12-2023 10:30 на корте 1 с оплатой False');
INSERT INTO userlog VALUES(39,1,'Создан новый блок расписания на  с 07-12-2023 08:00 по 07-12-2023 09:00 на корте 1 с оплатой True');
INSERT INTO userlog VALUES(40,1,'Удален блок расписания с id4');
INSERT INTO userlog VALUES(41,1,'Удален блок расписания с id5');
INSERT INTO userlog VALUES(42,1,'Удален блок расписания с id6');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	type VARCHAR(9), 
	fullname VARCHAR, 
	login VARCHAR, 
	password VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO users VALUES(1,'superuser','Администратор','admin','qwojndOQIWfoqiwfhqoiwfhoIWQHF');
INSERT INTO users VALUES(2,'api','api','api','qwkfoqopwfkqopwfkqpowfkqpowkfpoqwkfpok');
INSERT INTO users VALUES(3,'manager','manager1','manager1','QWF-21h9pqiwhfqw9fPWif');
INSERT INTO users VALUES(4,'manager','manager2','manager2','qwjQWfpoqwfjqpowfjWQPfojqwf');
INSERT INTO users VALUES(5,'manager','manager3','manager3','QWPOfjq90qw9jfq90wfjkqwjfpoiqwj');
INSERT INTO users VALUES(6,'manager','manager4','manager4','90qwj9ijhqwiofhqowfiqhwfoiqwqowf');
CREATE TABLE logins (
	id INTEGER NOT NULL, 
	user INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user) REFERENCES users (id)
);
CREATE INDEX ix_time_interval_objects_id ON time_interval_objects (id);
CREATE INDEX ix_clients_id ON clients (id);
CREATE INDEX ix_orders_id ON orders (id);
CREATE INDEX ix_typical_raspisanie_objects_id ON typical_raspisanie_objects (id);
CREATE INDEX ix_cort_id ON cort (id);
CREATE INDEX ix_userlog_id ON userlog (id);
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_logins_id ON logins (id);
COMMIT;
