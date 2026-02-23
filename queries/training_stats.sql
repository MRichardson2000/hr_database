with training_completers as (
    select e.first_name,
        e.last_name,
        t.course_name,
        t.completion_date
    from training t
    left join employees e on t.employee_id = e.employee_id
    where t.completion_date >= date('now', '-1 year')
)
select * from training_completers
where completion_date < date('now', '-180 days')
order by completion_date DESC