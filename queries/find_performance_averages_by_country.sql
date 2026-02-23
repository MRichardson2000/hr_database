with performance_scores as (
	select e.employee_id,
		   e.first_name,
		   e.last_name,
		   d.name as department_name, 
		   l.country,
		   p.score
	from employees e
	left join departments d on e.department_id = d.department_id
	left join performance p on e.employee_id = p.employee_id
	left join locations l on d.location_id = l.location_id
	where p.score >= 5
),
department_averages as (
	select department_name,
		   country, 
		   count(*) as total_reviews,
		   avg(score) as performance_average
	from performance_scores
	group by department_name, country
),
ranking_report as (
	select department_name,
		   country, 
		   total_reviews,
		   performance_average,
		   rank() over(order by performance_average desc) as country_ranking
	from department_averages
)

select * from ranking_report