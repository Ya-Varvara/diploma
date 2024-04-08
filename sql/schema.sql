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

INSERT INTO public.users (username, hashed_password, email, is_active, is_superuser, is_verified)
	VALUES ('admin', '$2b$12$3GGWjvTNrOCD6chPEDWSfeL14IzFXW2K449LzMIz6hx.o/etQj/mm', 'admin@gmail.com', true, false, false);

CREATE TABLE base_task_types (
    "id" serial NOT NULL,
	"name" text NOT NULL,
	"settings" json NOT NULL,

	PRIMARY KEY ("id")
);

INSERT INTO public.base_task_types (name, settings)
	VALUES ('граф', '{"nodes_number": "int", "min_weight": "int", "max_weight": "int"}');

CREATE TABLE task_types (
    "id" serial NOT NULL,
	"name" text NOT NULL,
 	"user_id" int NOT NULL,
	"base_task_type" int,
	"settings" json,
	"created_at" timestamp NOT NULL,
	"updated_at" timestamp NOT NULL,
	"deleted" bool NOT NULL,

	PRIMARY KEY ("id"),
	FOREIGN KEY ("user_id") REFERENCES users ("id"),
	FOREIGN KEY ("base_task_type") REFERENCES base_task_types ("id")
);

CREATE TABLE forms (
    "id" serial NOT NULL,
	"name" text NOT NULL,
    "short_name" text NOT NULL,
	"condition_form" bool NOT NULL,
	"answer_form" bool NOT NULL,

	PRIMARY KEY ("id")
);

INSERT INTO public.forms (name, short_name, condition_form, answer_form)
	VALUES 
	('таблица', 'table', true, false),
	('ввод', 'input', false, true),
	('выбор одного варианта', 'radio', false, true),
	('выбор нескольких вариантов варианта', 'checkbox', false, true),
	('загрузка файлов', 'upload', false, true),
	('текст', 'text', true, false);

CREATE TABLE task_types_condition_forms (
    "task_type_condition_form_id" int NOT NULL,
	"form_id" int NOT NULL,

	PRIMARY KEY ("task_type_condition_form_id", "form_id"),
	FOREIGN KEY ("task_type_condition_form_id") REFERENCES task_types ("id"),
	FOREIGN KEY ("form_id") REFERENCES forms ("id")
);

CREATE TABLE task_types_answer_forms (
    "task_type_answer_form_id" int NOT NULL,
	"form_id" int NOT NULL,

	PRIMARY KEY ("task_type_answer_form_id", "form_id"),
	FOREIGN KEY ("task_type_answer_form_id") REFERENCES task_types ("id"),
	FOREIGN KEY ("form_id") REFERENCES forms ("id")
);


CREATE TABLE tasks (
    "id" serial NOT NULL,
	"name" text NOT NULL,
	"type_id" int NOT NULL,
    "description_data" text NOT NULL,
	"condition_data" jsonb NOT NULL,
	"answer_data" jsonb NOT NULL,
	"user_id" int NOT NULL,
	"created_at" timestamp NOT NULL,
	"updated_at" timestamp NOT NULL,
	"deleted" bool NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("type_id") REFERENCES task_types ("id"),
	FOREIGN KEY ("user_id") REFERENCES users ("id")
);

CREATE TABLE tests (
    "id" serial NOT NULL,
	"name" text NOT NULL,
	"user_id" int NOT NULL,
	"start_datetime" timestamp NOT NULL,
	"end_datetime" timestamp NOT NULL,
	"test_time" time NOT NULL,
	"variants_number" int NOT NULL,
	"link" text NOT NULL,
	"created_at" timestamp NOT NULL,
	"updated_at" timestamp NOT NULL,
	"deleted" bool NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("user_id") REFERENCES users ("id")
);

CREATE TABLE test_task_types (
	"id" serial NOT NULL,
	"test_id" int NOT NULL,
	"task_type_id" int NOT NULL,
    "number" int NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("test_id") REFERENCES tests ("id"),
	FOREIGN KEY ("task_type_id") REFERENCES task_types ("id")
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
	"students_info" jsonb NOT NULL,
	"test_task_id" int NOT NULL,
	"answer" jsonb NOT NULL,
	"start_datetime" timestamp NOT NULL,
	"end_datetime" timestamp NOT NULL,
	"is_correct" bool,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("test_task_id") REFERENCES test_task ("id")
);

CREATE TABLE uploaded_files (
    "id" serial NOT NULL,
	"name" text NOT NULL,
	"path" text NOT NULL,
	"upload_date" timestamp NOT NULL,
	"test_task_id" int NOT NULL,
	
	PRIMARY KEY ("id"),
	FOREIGN KEY ("test_task_id") REFERENCES test_task ("id")
);