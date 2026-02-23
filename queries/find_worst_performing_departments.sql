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
        count(employee_id) as total_employees,
        sum(case when average_score <= 2 then 1 else 0 end) as poor_rating
    from employee_score
    group by department
    order by poor_rating desc
)
select * from employee_count
where dept_avg is not null
order by dept_avg asc
limit 2