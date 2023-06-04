
/* Drop Tables */

DROP TABLE IF EXISTS finance.usages;
DROP TABLE IF EXISTS finance.payment_types;
DROP TABLE IF EXISTS finance.sources;
DROP TABLE IF EXISTS finance.usage_categories;
DROP TABLE IF EXISTS master.users;




/* Create Tables */

CREATE TABLE finance.payment_types
(
	-- auto generated id
	payment_type_id serial NOT NULL UNIQUE,
	-- auto generated id
	source_id int NOT NULL UNIQUE,
	-- auto generated id
	user_id int NOT NULL UNIQUE,
	name varchar(50) NOT NULL,
	-- date that actual money is used
	payment_date date NOT NULL,
	-- display order
	order_no int NOT NULL,
	deleted boolean DEFAULT 'false' NOT NULL,
	PRIMARY KEY (payment_type_id),
	UNIQUE (payment_type_id, user_id)
) WITHOUT OIDS;


CREATE TABLE finance.sources
(
	-- auto generated id
	source_id serial NOT NULL UNIQUE,
	-- auto generated id
	user_id int NOT NULL UNIQUE,
	name varchar(50) NOT NULL,
	amount int DEFAULT 0 NOT NULL,
	-- color of source
	color_str varchar(20) NOT NULL,
	-- display order
	order_no int NOT NULL,
	deleted boolean DEFAULT 'false' NOT NULL,
	PRIMARY KEY (source_id),
	UNIQUE (source_id, user_id)
) WITHOUT OIDS;


CREATE TABLE finance.usages
(
	-- usage
	usage_id serial NOT NULL UNIQUE,
	-- auto generated id
	usage_category_id int NOT NULL UNIQUE,
	-- auto generated id
	payment_type_id int NOT NULL UNIQUE,
	-- auto generated id
	user_id int NOT NULL UNIQUE,
	name varchar(50) NOT NULL,
	place varchar(50),
	amount int NOT NULL,
	usage_date date NOT NULL,
	PRIMARY KEY (usage_id)
) WITHOUT OIDS;


CREATE TABLE finance.usage_categories
(
	-- auto generated id
	usage_category_id serial NOT NULL UNIQUE,
	-- auto generated id
	user_id int NOT NULL UNIQUE,
	name varchar(50) NOT NULL,
	amount int NOT NULL,
	-- color of source
	color_str varchar(20) NOT NULL,
	-- display order
	order_no int NOT NULL,
	deleted boolean DEFAULT 'false' NOT NULL,
	PRIMARY KEY (usage_category_id),
	UNIQUE (usage_category_id, user_id)
) WITHOUT OIDS;


CREATE TABLE master.users
(
	-- auto generated id
	user_id serial NOT NULL UNIQUE,
	-- Username to log in.
	username varchar(50) NOT NULL UNIQUE,
	-- encrypted password
	password bytea NOT NULL,
	-- user's email address
	email_address varchar(100) NOT NULL,
	-- user permission role
	user_role int NOT NULL,
	PRIMARY KEY (user_id)
) WITHOUT OIDS;



/* Create Foreign Keys */

ALTER TABLE finance.usages
	ADD FOREIGN KEY (payment_type_id, user_id)
	REFERENCES finance.payment_types (payment_type_id, user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE finance.payment_types
	ADD FOREIGN KEY (source_id, user_id)
	REFERENCES finance.sources (source_id, user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE finance.usages
	ADD FOREIGN KEY (usage_category_id)
	REFERENCES finance.usage_categories (usage_category_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE finance.sources
	ADD FOREIGN KEY (user_id)
	REFERENCES master.users (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE finance.usage_categories
	ADD FOREIGN KEY (user_id)
	REFERENCES master.users (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



/* Comments */

COMMENT ON COLUMN finance.payment_types.payment_type_id IS 'auto generated id';
COMMENT ON COLUMN finance.payment_types.source_id IS 'auto generated id';
COMMENT ON COLUMN finance.payment_types.user_id IS 'auto generated id';
COMMENT ON COLUMN finance.payment_types.payment_date IS 'date that actual money is used';
COMMENT ON COLUMN finance.payment_types.order_no IS 'display order';
COMMENT ON COLUMN finance.sources.source_id IS 'auto generated id';
COMMENT ON COLUMN finance.sources.user_id IS 'auto generated id';
COMMENT ON COLUMN finance.sources.color_str IS 'color of source';
COMMENT ON COLUMN finance.sources.order_no IS 'display order';
COMMENT ON COLUMN finance.usages.usage_id IS 'usage';
COMMENT ON COLUMN finance.usages.usage_category_id IS 'auto generated id';
COMMENT ON COLUMN finance.usages.payment_type_id IS 'auto generated id';
COMMENT ON COLUMN finance.usages.user_id IS 'auto generated id';
COMMENT ON COLUMN finance.usage_categories.usage_category_id IS 'auto generated id';
COMMENT ON COLUMN finance.usage_categories.user_id IS 'auto generated id';
COMMENT ON COLUMN finance.usage_categories.color_str IS 'color of source';
COMMENT ON COLUMN finance.usage_categories.order_no IS 'display order';
COMMENT ON COLUMN master.users.user_id IS 'auto generated id';
COMMENT ON COLUMN master.users.username IS 'Username to log in.';
COMMENT ON COLUMN master.users.password IS 'encrypted password';
COMMENT ON COLUMN master.users.email_address IS 'user''s email address';
COMMENT ON COLUMN master.users.user_role IS 'user permission role';



