with highest_earners as (
select e.employee_id,
    e.first_name,
    e.last_name,
    d.name as department,
    s.amount as employee_salary,
    rank() over (PARTITION by d.name order by s.amount desc) as earners_ranked
from employees e
left join departments d on e.department_id = d.department_id
left join salaries s on e.employee_id = s.employee_id	
)
select * from highest_earners where earners_ranked <= 3