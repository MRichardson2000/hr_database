select e.employee_id,
    e.first_name,
    e.last_name,
    d.name as department,
    j.title as job_title,
    count(*) as completed_training_courses
from employees e 
left join departments d on e.department_id = d.department_id
left join jobs j on e.job_id = j.job_id
left join training t on e.employee_id = t.employee_id
group by e.employee_id
order by completed_training_courses DESC
limit 5