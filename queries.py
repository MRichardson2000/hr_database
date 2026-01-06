from database.dbconn import fetch_result
from typing import Any


def find_highest_paid_employees() -> list[dict[str, Any]]:
    return fetch_result(
        """
        with employee_salaries as (
        select e.employee_id,
            e.first_name,
            e.last_name,
            j.title,
            d.name,
            avg(s.amount) as average_salary
        from employees e
        left join jobs j on e.job_id = j.job_id
        left join departments d on e.department_id = d.department_id
        left join salaries s on e.employee_id = s.employee_id
        where s.amount is not null
        group by e.employee_id
        order by average_salary desc
        )
        select * from employee_salaries
        limit 10
        """
    )


def find_top_absent_employees() -> list[dict[str, Any]]:
    return fetch_result(
        """
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
        """
    )


def find_top_five_training_completers() -> list[dict[str, Any]]:
    return fetch_result(
        """
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
        """
    )


def find_top_five_projects() -> list[dict[str, Any]]:
    return fetch_result(
        """
        select p.name,
                    d.name,
                    p.start_date,
                    p.end_date,
                    julianday(p.end_date) - julianday(p.start_date) as duration
        from projects p
        left join departments d on p.department_id = d.department_id
        order by duration DESC
        limit 5
        """
    )


def find_performance_averages() -> list[dict[str, Any]]:
    return fetch_result(
        """
        with employee_score as (
            select e.employee_id,
                d.name as department_name,
                avg(p.score) as average_score
            from employees e
            left join departments d on e.department_id = d.department_id
            left join performance p on e.employee_id = p.employee_id
            group by e.employee_id
        )
        select department_name,
            avg(average_score) as dept_avg,
            count(employee_id) as total_employees,
            sum(case when average_score = 5 then 1 else 0 end) as excellent_count,
            sum(case when average_score = 4 then 1 else 0 end) as good_count,
            sum(case when average_score = 3 then 1 else 0 end) as average_count,
            sum(case when average_score <= 2 then 1 else 0 end) as poor_count
        from employee_score
        group by department_name
        having avg(average_score) < 3
        """
    )


def find_deps_with_poor_employee_stats() -> list[dict[str, Any]]:
    return fetch_result(
        """
        with employee_score as (
            select e.employee_id,
                d.name as department,
                avg(p.score) as average_score
            from employees e
            left join departments d on e.department_id = d.department_id
            left join performance p  on e.employee_id = p.employee_id
            group by e.employee_id
        ),
        employee_counts as (
            select department,
                avg(average_score) as dept_avg,
                count(employee_id) as total_employees,
                sum(case when average_score <= 2 then 1 else 0 end) as poor_count,
                sum(case when average_score <= 2 then 1 else 0 end) * 100 / count(employee_id) as poor_percentage 
        from employee_score
        group by department
        having count(employee_id) >= 5
        order by poor_percentage DESC
        limit 3
        )
        select * from employee_counts
        """
    )


def find_top_two_depts_scores() -> list[dict[str, Any]]:
    return fetch_result(
        """
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
                    count(employee_id) as total_employees
                from employee_score
                group by department
            )
            select * from employee_count
            order by dept_avg DESC
            limit 2
        """
    )


def find_worst_performing_departments() -> list[dict[str, Any]]:
    return fetch_result(
        """
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
        """
    )


def find_dept_with_widest_performance_gap() -> list[dict[str, Any]]:
    return fetch_result(
        """
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
    """
    )


def find_top_five_salaries() -> list[dict[str, Any]]:
    return fetch_result(
        """
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
        """
    )


def salary_ranking() -> list[dict[str, Any]]:
    return fetch_result(
        """
        select e.employee_id,
               d.name,
               s.amount,
               s.effective_date,
               rank () over (partition by d.name order by s.amount desc) as salary_ranking
            from salaries s
            left join employees e on e.employee_id = s.employee_id
            left join departments d on e.department_id = d.department_id
        """
    )


def main() -> None:
    pass


if __name__ == "__main__":
    main()
