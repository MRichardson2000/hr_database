with employee_score as (
    select e.employee_id,
        d.name as department,
        avg(p.score) as average_score
    from employees e
    left join departments d on e.department_id = d.department_id
    left join performance p  on e.employee_id = p.employee_id
    group by e.employee_id
),
employee_counts as (
    select department,
        avg(average_score) as dept_avg,
        count(employee_id) as total_employees,
        sum(case when average_score <= 2 then 1 else 0 end) as poor_count,
        sum(case when average_score <= 2 then 1 else 0 end) * 100 / count(employee_id) as poor_percentage 
from employee_score
group by department
having count(employee_id) >= 5
order by poor_percentage DESC
limit 3
)
select * from employee_counts