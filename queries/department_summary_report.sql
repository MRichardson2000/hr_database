select
	d.name as department_name,
	count(e.employee_id) as total_employees,
	sum(case when p.score >= 4 then 1 else 0 end) as high_performers,
	sum(case when p.score <= 2 then 1 else 0 end) as low_performers,
	sum(case when e.hire_date >= date('now', '-730 day') then 1 else 0 end) as recent_hires,
	sum(case when a.status = 'Remote' and a.date >= date('now', '-30 day') then 1 else 0 end) as num_remote_days_last_30
from employees e
left join attendance a on e.employee_id = a.employee_id
left join departments d on e.department_id = d.department_id
left join performance p on e.employee_id = p.employee_id
group by d.name
