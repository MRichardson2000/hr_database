select p.name,
            d.name,
            p.start_date,
            p.end_date,
            julianday(p.end_date) - julianday(p.start_date) as duration
from projects p
left join departments d on p.department_id = d.department_id
order by duration DESC
limit 5