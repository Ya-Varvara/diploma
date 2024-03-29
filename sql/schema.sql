CREATE TABLE users (
    "id" serial NOT NULL,
	"username" text NOT NULL,
	"hashed_password" text NOT NULL,
    "email" text NOT NULL,
	-- "meta" jsonb NOT NULL,
	"is_active" bool NOT NULL default true,
	"is_superuser" bool NOT NULL default false,
	"is_verified" bool NOT NULL default false,
	
	PRIMARY KEY ("id")
);

INSERT INTO public.users(
	id, username, hashed_password, email, is_active, is_superuser, is_verified)
	VALUES (1, 'admin', '$2b$12$3GGWjvTNrOCD6chPEDWSfeL14IzFXW2K449LzMIz6hx.o/etQj/mm', 'admin@gmail.com', true, false, false);

CREATE TABLE task_types (
    "id" serial NOT NULL,
	"name" text NOT NULL,
    "data_types" text[] NOT NULL,
    "answer_type" text[] NOT NULL,
	"user_id" int NOT NULL,

	PRIMARY KEY ("id"),
	FOREIGN KEY ("user_id") REFERENCES users ("id")
);

CREATE TABLE tasks (
    "id" serial NOT NULL,
	"name" text NOT NULL,
	"type_id" int NOT NULL,
    "data" jsonb NOT NULL,
	"user_id" int NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("type_id") REFERENCES task_types ("id"),
	FOREIGN KEY ("user_id") REFERENCES users ("id")
);

CREATE TABLE tests (
    "id" serial NOT NULL,
	"name" text NOT NULL,
	"user_id" int NOT NULL,
    "description" jsonb NOT NULL,
	"link" text NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("user_id") REFERENCES users ("id")
);

CREATE TABLE test_task (
    "id" serial NOT NULL,
	"variant" int NOT NULL,
	"test_id" int NOT NULL,
	"task_id" int NOT NULL,
    "is_given" bool NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("test_id") REFERENCES tests ("id"),
	FOREIGN KEY ("task_id") REFERENCES tasks ("id")
);

CREATE TABLE test_task_result (
    "id" serial NOT NULL,
	"student_info" jsonb NOT NULL,
	"test_task_id" int NOT NULL,
	"answer" jsonb NOT NULL,
	"data" bytea,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("test_task_id") REFERENCES test_task ("id")
);
