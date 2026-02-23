with employee_wages as (
select e.employee_id,
        e.first_name,
        e.last_name,
        d.name as department, 
        s.amount as employee_salary, 
        avg(s.amount) over (partition by d.name) as department_average 
from employees e 
left join departments d on e.department_id = d.department_id 
left join salaries s on e.employee_id = s.employee_id	 
where s.amount is not null 
) 
select * from employee_wages where employee_salary > department_average