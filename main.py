from utils import run_sql, run_plain_sql

create_table_animals = '''
create table animals_OPT (
    animal_id integer primary key autoincrement,
    animal_type varchar(10),
    name varchar(20),
    breed1 varchar(30),
    breed2 varchar(30),    
    color1 varchar(20),
    color2 varchar(20),
    date_of_birth date,
    outcome_subtype varchar(20),
    outcome_type varchar(20),
    outcome_date date,
    outcome_subtype_id integer,
    outcome_type_id integer,
    breed1_id integer,
    breed2_id integer,    
    color1_id integer,
    color2_id integer,
    animal_type_id integer,
    foreign key (outcome_subtype_id) references outcome_subtypes(id),
    foreign key (outcome_type_id) references outcome_types(id)--,        
--    foreign key (breed1_id) references breeds(id),        
--    foreign key (breed2_id) references breeds(id) --,        
--    foreign key (color1_id) references colors(id),        
--    foreign key (color2_id) references colors(id)        
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
where outcome_subtype is not null
order by outcome_subtype
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
where outcome_type is not null
order by outcome_type
'''

create_table_breeds = '''
create table breeds (
    id integer primary key autoincrement,
    breed varchar(30)
)
'''

fill_in_breeds = '''
insert into breeds (breed)
    select distinct breed
    from (
    select
        case when instr(breed, '/')=0 then trim(breed)
        else trim(substr(breed, 1, instr(breed, '/')-1)) end breed
    from animals
    union all
    select
        case when instr(breed, '/')=0 then null
        else trim(substr(breed, instr(breed, '/')+1)) end breed
    from animals)
    where breed is not null
    order by 1
'''

create_table_animal_types = '''
create table animal_types (
    id integer primary key autoincrement,
    animal_type varchar(20)
)
'''

fill_in_animal_types = '''
insert into animal_types (animal_type)
    select distinct animal_type
    from animals
    where animal_type is not null
    order by 1
'''

create_table_animals_colors = '''
create table animals_colors (
    id integer primary key autoincrement,
    animal_id int,
    color_id int,
    foreign key (color_id) references colors(id),
    foreign key (animal_id) references animals_OPT(animal_id)
)
'''

fill_in_animals_colors = '''
insert into animals_colors (animal_id, color_id)
    select animal_id,
        color1_id color_id
    from animals_OPT
    where color_id is not null
    union all
    select animal_id,
        color2_id color_id
    from animals_OPT
    where color_id is not null
    order by animal_id    
'''

create_table_animals_breeds = '''
create table animals_breeds (
    id integer primary key autoincrement,
    animal_id int,
    breed_id int,
    foreign key (breed_id) references breeds(id),
    foreign key (animal_id) references animals_OPT(animal_id)
)
'''

fill_in_animals_breeds = '''
insert into animals_breeds (animal_id, breed_id)
    select animal_id,
        breed1_id breed_id
    from animals_OPT
    where breed_id is not null
    union all
    select animal_id,
        breed2_id breed_id
    from animals_OPT
    where breed_id is not null
    order by animal_id    
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
insert into animals_OPT (animal_type, name, breed1, breed2, color1, color2, date_of_birth,
    outcome_subtype, outcome_type, outcome_date, outcome_subtype_id, outcome_type_id, breed1_id,
    breed2_id, color1_id, color2_id, animal_type_id)

select 
    a.animal_type,
    name,
    case when instr(a.breed, '/')=0 then trim(a.breed)
        else substr(a.breed, 1, instr(a.breed, '/')-1) end breed1,
    case when instr(a.breed, '/')=0 then null
        else substr(a.breed, instr(a.breed, '/')+1) end breed2,        
    trim(color1),
    trim(color2),    
    date(date_of_birth) date_of_birth,
    outcome_subtype,
    outcome_type,
    date(outcome_year || '-' || printf('%02d', outcome_month) || '-01') outcome_date
    , o.id
    , ot.id id2
    , b.id id3
    , bb.id id4
    , c.id id5
    , cc.id id6
    , at.id id7
from animals a
    left join outcome_subtypes o using (outcome_subtype)
    left join outcome_types ot using (outcome_type)
    left join breeds b on breed1 = b.breed
    left join breeds bb on breed2 = bb.breed
    left join colors c on trim(a.color1) = c.color
    left join colors cc on trim(a.color2) = cc.color
    left join animal_types at on a.animal_type = at.animal_type
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

sql_rename = '''
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
where color is not null
order by color
'''


def create_all():
    run_plain_sql('drop table if exists animal_types')
    run_plain_sql(create_table_animal_types)
    run_plain_sql(fill_in_animal_types)

    run_plain_sql('drop table if exists breeds')
    run_plain_sql(create_table_breeds)
    run_plain_sql(fill_in_breeds)

    run_plain_sql('drop table if exists colors')
    run_plain_sql(create_table_colors)
    run_plain_sql(fill_in_colors)

    run_plain_sql('drop table if exists outcome_subtypes')
    run_plain_sql(create_table_outcome_subtypes)
    run_plain_sql(fill_in_outcome_subtypes)

    run_plain_sql('drop table if exists outcome_types')
    run_plain_sql(create_table_outcome_types)
    run_plain_sql(fill_in_outcome_types)

    run_plain_sql('drop table if exists animals_OPT')
    run_plain_sql(create_table_animals)
    run_plain_sql(transfer_data)
    #
    run_plain_sql('drop table if exists animals_colors')
    run_plain_sql(create_table_animals_colors)
    run_plain_sql(fill_in_animals_colors)
    #
    run_plain_sql('drop table if exists animals_breeds')
    run_plain_sql(create_table_animals_breeds)
    run_plain_sql(fill_in_animals_breeds)
    #
    run_plain_sql('alter table animals_OPT drop column outcome_subtype')
    run_plain_sql('alter table animals_OPT drop column outcome_type')
    run_plain_sql('alter table animals_OPT drop column color1')
    run_plain_sql('alter table animals_OPT drop column color2')
    run_plain_sql('alter table animals_OPT drop column breed1')
    run_plain_sql('alter table animals_OPT drop column breed2')
    run_plain_sql('alter table animals_OPT drop column animal_type')
    run_plain_sql('alter table animals_OPT drop column breed1_id')
    run_plain_sql('alter table animals_OPT drop column breed2_id')
    run_plain_sql('alter table animals_OPT drop column color1_id')
    run_plain_sql('alter table animals_OPT drop column color2_id')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create_all()  # creates all tables and transfers all data; uncomment if you want to recreate all tables

    # some views
    # print(run_sql('select count(*) "animals lines" from animals'))
    # print(run_sql('select count(*) "animals_OPT lines" from animals_OPT'))
    # print('Table Animals (original)')
    # print(run_sql('select * from animals limit 12'))
    # print('Table Animals_OPT (optimized)')
    # print(run_sql('select * from animals_OPT limit 12'))
    # print(run_sql('select * from animals_colors where animal_id = 10 limit 12'))
    # print(run_sql('select * from animals_colors limit 5'))
    # print(run_sql('select * from animals_breeds limit 5'))
    # print(run_sql('''
    # select animal_id, count(animal_id)
    # from animals_breeds
    # group by 1
    # having count(animal_id) > 1
    # limit 5
    # '''))

    print(run_sql('''
        with breeds_lst as (
            select animal_id, 
                group_concat(b.breed, '/') breed_lst
            from animals_breeds ab
                left join breeds b on ab.breed_id = b.id
            group by 1
            ),
        colors_lst as (
            select animal_id,
                group_concat(c.color, '/') color_lst
            from animals_colors ac
                left join colors c on ac.color_id = c.id
            group by 1
            )
        select at.animal_type animal_type,
            name,
            date_of_birth,
            outcome_date,
            o.outcome_subtype,
            ot.outcome_type,
            color_lst,
            breed_lst
        from animals_OPT a
            left join outcome_subtypes o on a.outcome_subtype_id = o.id
            left join outcome_types ot on a.outcome_type_id = ot.id
            left join animal_types at on a.animal_type_id = at.id
            left join colors_lst using (animal_id)
            left join breeds_lst using (animal_id)
        limit 5
        '''))

    # tests -------------
    assert run_plain_sql('select count(*) from animals')[0][0] \
           == run_plain_sql('select count(*) from animals_OPT')[0][0], "Tables contain a different number of lines"

    assert run_plain_sql('select count(*) from outcome_subtypes where outcome_subtype is null')[0][0] == 0,\
        "There are null outcome_subtypes"

    assert run_plain_sql('select count(*) from outcome_types where outcome_type is null')[0][0] == 0,\
        "There are null outcome_types"

    assert run_plain_sql('select count(*) from colors where color is null')[0][0] == 0,\
        "There are null colors"

    assert run_plain_sql('select count(*) from breeds where breed is null')[0][0] == 0,\
        "There are null breeds"

    assert run_plain_sql('''
    select count(distinct color)
    from ( 
        select distinct trim(color1) color
        from animals
        where color1 is not null
        union all
        select distinct trim(color2) color 
        from animals
        where color2 is not null
    )    
    ''')[0][0] == run_plain_sql('''
    select count(color)
    from colors
    ''')[0][0], "Number of colors is not equal"

    assert run_plain_sql('''
    select count(distinct outcome_subtype)
    from animals 
    where outcome_subtype is not null
    ''')[0][0] == run_plain_sql('''
    select count(outcome_subtype)
    from outcome_subtypes
    ''')[0][0], "Number of outcome_subtypes is not equal"

    assert run_plain_sql('''
    select count(distinct outcome_type)
    from animals 
    where outcome_type is not null
    ''')[0][0] == run_plain_sql('''
    select count(outcome_type)
    from outcome_types
    ''')[0][0], "Number of outcome_types is not equal"

    assert run_plain_sql('''
    select count(name)
    from animals
    ''')[0][0] == run_plain_sql('''
    select count(name)
    from animals_OPT
    ''')[0][0], "Number of names is not equal"

    assert run_plain_sql('''
    select sum(date(date_of_birth))
    from animals
    ''')[0][0] == run_plain_sql('''
    select sum(date(date_of_birth))
    from animals_OPT
    ''')[0][0], "Dates of birth are not equal"
    # end of tests ------------
