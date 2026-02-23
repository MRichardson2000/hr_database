with training_completers as(
	select distinct e.employee_id,
					e.first_name,
					e.last_name,
					d.department_id,
					l.country
	from employees e
	left join training t on e.employee_id = t.employee_id
	left join departments d on e.department_id = d.department_id
	left join locations l on d.location_id = l.location_id
	where completion_date is not null
	and course_name is not null
),

training_completers_with_country as (
	select employee_id,
		   first_name, 
		   last_name,
		   country
	from training_completers
),

group_trainees_by_country as (
	select country, count(employee_id) as total_training_completers
	from training_completers_with_country
	group by country
),

rank_by_countries as (
	select country, 
	total_training_completers,
		   rank () over(order by total_training_completers desc) as highest_training_completers
	from group_trainees_by_country
)

select *
from rank_by_countries
where highest_training_completers < 5

