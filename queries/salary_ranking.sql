select e.employee_id,
    d.name,
    s.amount,
    s.effective_date,
    rank () over (partition by d.name order by s.amount desc) as salary_ranking
from salaries s
left join employees e on e.employee_id = s.employee_id
left join departments d on e.department_id = d.department_id