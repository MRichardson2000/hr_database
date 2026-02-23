select p.name as project_name,
    d.name as department_name,
    count(distinct e.employee_id) as total_employees,
    count(distinct t.employee_id) as training_completers,
    count(distinct t.employee_id) * 100.0 / count(distinct e.employee_id) as training_coverage
from employees e
left join departments d on e.department_id = d.department_id
left join projects p on p.department_id = d.department_id
left join training t on e.employee_id = t.employee_id
group by project_name, department_name
having project_name is not null