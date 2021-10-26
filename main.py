import sqlite3
import prettytable


def run_sql(sql_):
    with sqlite3.connect('animal.db') as conn:
        cur = conn.cursor()
        results = cur.execute(sql_)
        my_table = prettytable.from_db_cursor(results)
        my_table.max_width = 30
        return my_table


def run_plain_sql(sql_):
    with sqlite3.connect('animal.db') as conn:
        cur = conn.cursor()
        return cur.execute(sql_).fetchall()


create_table_animals = '''
create table animals_OPT (
    animal_id integer primary key autoincrement,
    animal_type varchar(10),
    name varchar(20),
    breed varchar(40),
    color varchar(30),
    date_of_birth date,
    outcome_subtype varchar(20),
    outcome_type varchar(20),
    outcome_date date,
    outcome_subtype_id integer,
    outcome_type_id integer,
    breed_id integer,
    constraint fk_outcome_subtypes
        foreign key (outcome_subtype_id)
        references outcome_subtypes(id),
    constraint fk_outcome_types
        foreign key (outcome_type_id)
        references outcome_types(id)        
    constraint fk_breeds
        foreign key (breed_id)
        references breeds(id)        
)
'''


create_table_outcome_subtypes = '''
create table outcome_subtypes (
    id integer primary key autoincrement,
    outcome_subtype varchar(20)
)
'''

fill_in_outcome_subtypes = '''
insert into outcome_subtypes (outcome_subtype)
select distinct outcome_subtype
from animals
'''


create_table_outcome_types = '''
create table outcome_types (
    id integer primary key autoincrement,
    outcome_type varchar(20)
)
'''

fill_in_outcome_types = '''
insert into outcome_types (outcome_type)
select distinct outcome_type
from animals
'''

create_table_breeds = '''
create table breeds (
    id integer primary key autoincrement,
    breed varchar(40)
)
'''

fill_in_breeds = '''
insert into breeds (breed)
select distinct breed
from animals
'''



sql2 = '''
insert into animals (animal_type, age_upon_outcome) values
('Кошка', 2)
'''


sql3 = '''
update animals
set animal_type = 'Кошка' where animal_type = 'Кот'
'''


sql4 = '''
alter table animals
add column name2 nvarchar(20)
'''

sql5 = '''
select distinct substr(age_upon_outcome, instr(age_upon_outcome, ' ')) as age
from animals
order by length(age)
limit 10
'''

sql6 = '''
select color1, color2 , length(color1)+length(color2)
from animals
where color2 is not null
order by 3 desc
limit 10
'''


# shows max length of string fields
sql7 = '''
with 
animal_type as (
    select 'animal_type', animal_type "contents", length(animal_type) "max length"
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    ),
name as (
    select 'name', name, length(name)
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    ),
breed as (
    select 'breed', breed, length(breed)
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    ),
color1 as (
    select 'color1', color1, length(color1)
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    ),
color2 as (
    select 'color2', color2, length(color2)    
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    ),
outcome_subtype as (
    select 'outcome_subtype', outcome_subtype, length(outcome_subtype)
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    ),
outcome_type as (
    select 'outcome_type', outcome_type, length(outcome_type)
    from animals
    group by 1,2
    order by 3 desc 
    limit 1
    )

select * from animal_type
union all
select * from name
union all
select * from breed
union all
select * from color1
union all
select * from color2
union all
select * from outcome_subtype
union all
select * from outcome_type
'''


transfer_data = '''
insert into animals_OPT (animal_type, name, breed, color, date_of_birth, outcome_subtype, outcome_type,
    outcome_date, outcome_subtype_id, outcome_type_id)

select 
    animal_type,
    name,
    breed,
    case
        when color1 is not null and color2 is not null then trim(color1) || ', ' || trim(color2)
        else
            (case when color1 is not null then trim(color1)
            else trim(color2) end)
        end as color,
        
    date(date_of_birth) date_of_birth,
    outcome_subtype,
    outcome_type,
    date(outcome_year || '-' || printf('%02d', outcome_month) || '-01') outcome_date
    , o.id
    , ot.id id2
from animals a
    join outcome_subtypes o
        using (outcome_subtype)
    join outcome_types ot
        using (outcome_type)
'''


sql_outcome_types = '''
select distinct outcome_type
from animals
'''


sql_outcome_subtypes = '''
select distinct outcome_subtype
from animals
'''

sql_length_of_columns = '''
select animal_id,
    name,
    length(name),
    length(breed),
    length(color1),
    length(date_of_birth)
from animals
limit 10
'''


sql_ref = '''
alter table animals_OPT rename to animals_old
'''

# add column outcome_subtype_id int
# add foreign key (outcome_subtype_id) references outcome_subtypes(id)

# pragma foreign_keys = on;
# drop column outcome_subtype_id

# alter column name nvarchar(20) constraint df_name default 'Noname'

create_table_colors = '''
create table colors (
    id integer primary key autoincrement,
    color varchar(20)
)
'''

fill_in_colors = '''
insert into colors (color)
select distinct trim(color) color 
from (select distinct color1 color from animals
    union all
    select distinct color2 color from animals)
'''



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # run_plain_sql('drop table animals_OPT')

    # run_plain_sql(create_table_breeds)
    # run_plain_sql(fill_in_breeds)

    # run_plain_sql(create_table_animals)
    # run_plain_sql(transfer_data)
    # run_plain_sql('alter table animals_OPT drop column outcome_subtype')
    # run_plain_sql('alter table animals_OPT drop column outcome_type')
    # results = run_sql('select * from animals_OPT limit 5')

    # run_plain_sql('drop table colors')
    # run_plain_sql(create_table_colors)
    # run_plain_sql(fill_in_colors)

    # results = run_sql('select breed, count(*) from animals_OPT group by 1 order by 2 desc')
    # results = run_sql('''
    # select count(distinct trim(color)) color from (select distinct color1 color from animals
    # union all
    # select distinct color2 color from animals)
    # order by color
    # ''')

    results = run_sql('select * from animals_OPT limit 5')

    print(results)



