with employee_score as (
    select e.employee_id,
        d.name as department_name,
        avg(p.score) as average_score
    from employees e
    left join departments d on e.department_id = d.department_id
    left join performance p on e.employee_id = p.employee_id
    group by e.employee_id
)
select department_name,
    avg(average_score) as dept_avg,
    count(employee_id) as total_employees,
    sum(case when average_score = 5 then 1 else 0 end) as excellent_count,
    sum(case when average_score = 4 then 1 else 0 end) as good_count,
    sum(case when average_score = 3 then 1 else 0 end) as average_count,
    sum(case when average_score <= 2 then 1 else 0 end) as poor_count
from employee_score
group by department_name
having avg(average_score) < 3