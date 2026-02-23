with employee_score as (
    select e.employee_id,
        d.name as department,
        avg(p.score) as average_score
from employees e
left join departments d on e.department_id = d.department_id
left join performance p on e.employee_id = p.employee_id
group by e.employee_id
),
employee_count as (
    select department,
        avg(average_score) as dept_avg,
        count(employee_id) as total_employees
    from employee_score
    group by department
)
select * from employee_count
order by dept_avg DESC
limit 2