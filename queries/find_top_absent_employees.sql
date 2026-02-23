select e.employee_id,
    e.first_name,
    e.last_name,
    d.name as department_name,
    count(*) as total_absences
from employees e
left join departments d on e.department_id = d.department_id
left join attendance a on e.employee_id = a.employee_id
where status = 'Absent'
    and a.date >= date('now', '-1 year')
group by
    e.employee_id
order by total_absences desc
limit 10