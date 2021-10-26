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
        cur.execute(sql_)


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
    outcome_date date
)
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
    outcome_date)

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
from animals

'''


sql_outcome_types = '''
select distinct outcome_type
from animals
'''


sql_outcome_subtypes = '''
select distinct outcome_subtype
from animals
'''



# alter column name nvarchar(20) constraint df_name default 'Noname'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # run_plain_sql(transfer_data)
    # print(run_sql('select * from animals limit 5'))
    # print(run_sql('select count(*) from animals_OPT'))
    print(run_sql(sql_outcome_subtypes))
