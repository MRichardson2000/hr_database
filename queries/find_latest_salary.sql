with employee_details as (
	select 
	e.employee_id,
	e.first_name,
	e.last_name,
	d.name as department_name,
	j.title as job_title,
	s.amount as salary,
	s.effective_date,
	row_number() over(partition by e.employee_id order by s.effective_date desc) as employee_salaries
	from
	employees e
	left join salaries s on e.employee_id = s.employee_id
	left join departments d on e.department_id = d.department_id
	left join jobs j on e.job_id = j.job_id
)
select * from employee_details
where employee_salaries = 1
