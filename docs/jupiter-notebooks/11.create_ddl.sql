create table programs(
	id integer primary key autoincrement not null,
	
	name varchar(100) not null
);


create table students(
	id integer primary key autoincrement not null,
	program_id integer not null,

	card varchar(10) not null,

	surname varchar(20) not null,
	name varchar(20) not null,
	patronymic varchar(20) null,
	
	foreign key(program_id) references programs(id)
);

create unique index students_card on students(card);
create index students_names on students(surname, name, patronymic);

create table courses(
	id integer primary key autoincrement not null,
	name varchar(200) not null
);

create table programs_courses(
	semester_number int not null,
	course_id int not null,
	program_id int not null,
	
	primary key(semester_number, course_id, program_id),
	foreign key(course_id) references course(id),
	foreign key(program_id) references program(id)
);

create table marks(
	student_id int not null,
	course_id int not null,
	mark int not null,
	
	primary key(course_id, student_id),
	foreign key(student_id) references student(id),
	foreign key(course_id) references course(id)
);
