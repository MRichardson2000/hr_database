select e.employee_id,
    e.first_name,
    e.last_name,
    j.title,
    max(s.amount) as salary
from employees e
left join jobs j on e.job_id = j.job_id
left join salaries s on e.employee_id = s.employee_id
where s.amount is not null
group by e.employee_id
order by salary desc
limit 5