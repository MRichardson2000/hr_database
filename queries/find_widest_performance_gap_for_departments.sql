with employee_score as (
select e.employee_id,
    d.name as department,
    avg(p.score) as average_score
from employees e
left join departments d on e.department_id = d.department_id
left join performance p on e.employee_id = p.employee_id
group by e.employee_id
),
performance_gap as (
    select department,
    max(average_score) as max_score,
    min(average_score) as min_score,
    (max(average_score) - min(average_score)) as gap
from employee_score
group by department
having max(average_score) - min(average_score) > 0
)
select department, gap, max(gap) over() as max_gap
from performance_gap
where gap = (select max(gap) from performance_gap)
order by gap desc