with employee_details as (
select
 e.employee_id,
 e.first_name,
 e.last_name,
 d.department_id,
 d.name as department_name,
 s.effective_date,
 s.amount as salary,
 row_number() over(partition by e.employee_id order by s.effective_date desc) as salary_rankings
from employees e
left join departments d on e.department_id = d.department_id
left join salaries s on e.employee_id = s.employee_id
),

top_salary as (
	select  
	 department_id,
	 department_name,
	 employee_id,
	 first_name,
	 last_name,
	 effective_date,
	 salary
	from employee_details
	where salary_rankings = 1
),
employee_salaries_per_department as (
	select 
	 department_id, 
	 department_name,
	 employee_id,
	 first_name,
	 last_name,
	 effective_date,
	 salary,
	 rank() over(partition by department_id order by salary desc) as department_salary_rank
	from top_salary
)

select * from employee_salaries_per_department
where department_salary_rank <= 3