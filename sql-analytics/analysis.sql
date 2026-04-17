-- #4 Top 3 customers by total spending

-- Total spending of all customers
with cte as(
select customer_id, sum(price*quantity) total_spent
from order_items oi
join orders o
	on oi.order_id = o.order_id
    and o.status = 'Completed'
group by customer_id)

-- Selecting top 3 customers
select *
from (select *, rank() over(order by total_spent desc) customer_rank
from cte) t
where customer_rank <= 3;


-- #7 Monthly revenue trend

-- Total Revenue by month
with cte as(
select substring(order_date,1,7) month, sum(oi.price*quantity) revenue
from order_items oi
join orders o
	on oi.order_id = o.order_id
    and status = 'Completed'
group by substring(order_date,1,7)
)

-- Calculating the month-to-month difference
select *, revenue - lag(revenue) over(order by month) diff_last_month
from cte;


-- #9 Rank products by revenue within category

-- Total product revenue
with cte as(
select product_name, category_name, sum(oi.price*quantity) revenue
from order_items oi
join orders o
	on oi.order_id = o.order_id
    and o.status = 'Completed'
join products p
	on oi.product_id = p.product_id
join categories c
	on p.category_id = c.category_id
group by  product_name, category_name)

-- Ranking products within the category
select *, rank() over(partition by category_name order by revenue desc) revenue_rank
from cte;


-- #11 Split customers into: “low” (< 100 total spend, “medium” (100–500), “high” (> 500)

-- Calculating CLV and the respective segment
with cte as
(
select customer_id, sum(oi.price*quantity) CLV,
case when sum(oi.price*quantity) < 100 then 'Low'
	 when sum(oi.price*quantity) between 100 and 500 then 'Medium'
     else 'High'
end segment
from order_items oi
join orders o
	on oi.order_id = o.order_id
    and status = 'Completed'
group by customer_id)

-- Counting custmoers in each segment and total segment revenue
select segment, count(customer_id) num_of_customers, sum(CLV) segment_rev
from cte
group by segment;


-- #15 What % of total revenue comes from the top 20% of customers?

-- Calculating CLV
with cte as(
select customer_id, sum(oi.price*quantity) CLV
from order_items oi
join orders o
	on oi.order_id = o.order_id
    and status = 'Completed'
group by customer_id),

-- Calculatign total revenue for everyone and for top 20% customers
cte2 as (select sum(CLV) top_20_perc_rev, (select sum(CLV) from cte) hundred_perc_rev
from (select *, ntile(5) over(order by CLV desc) percent_group
from cte) t
where percent_group = 1)

select top_20_perc_rev/hundred_perc_rev top_20_perc
from cte2;


-- #16 Find the most common pairs of products bought together in the same order

select p1.product_name, p2.product_name, count(distinct oi1.order_id) times_bought
from order_items oi1
join order_items oi2
	on oi1.order_id = oi2.order_id
	and oi1.product_id != oi2.product_id
    and oi1.product_id < oi2.product_id
join products p1
	on oi1.product_id = p1.product_id
join products p2
	on oi2.product_id = p2.product_id
join orders o
	on oi1.order_id = o.order_id
where status = 'Completed'
group by oi1.product_id, oi2.product_id;


-- #17 For each customer, determine whether they are retained: A customer is retained if they made another purchase within 30 days of their first order

-- Numbering each customer's orders based on date
with cte as(
select customer_id,order_date, row_number() over(partition by customer_id order by order_date) customers_order
from orders o1
where o1.status = 'completed')


-- Finding retention
select cte1.customer_id, cte1.order_date first_order, cte2.order_date second_order,
case when datediff(cte2.order_date, cte1.order_date) <= 30 then 'Retained'
	else 'Not retained'
end retainment
from cte as cte1
left join cte as cte2
	on cte1.customer_id = cte2.customer_id
    and cte2.customers_order = 2
where cte1.customers_order = 1;


-- #18 Analyze how each customer's spending behavior changes over time

-- Total revenue per order
with cte1 as(
select c.customer_id, o.order_id, date_format(order_date,"%Y-%m") `month`, row_number() over(partition by customer_id order by order_date) order_number, sum(oi.quantity*oi.price) order_revenue
from orders o
join customers c
	on o.customer_id = c.customer_id
join order_items oi
	on o.order_id = oi.order_id
where o.status = 'Completed'
group by order_id),

-- Revenue by customer and month
cte2 as (
select customer_id, `month`, sum(order_revenue) monthly_revenue
from cte1
group by customer_id, `month`),

-- Revenue change from the previous month
cte3 as(
select *, coalesce(lag(monthly_revenue) over(partition by customer_id),0) previous_month_revenue, coalesce(monthly_revenue - lag(monthly_revenue) over(partition by customer_id),0) revenue_change
from cte2),

-- Assigning labels
cte4 as (
select *,
case when growth_rate_perc > 50 then 'increase'
	 when growth_rate_perc < -50 then 'decrease'
     else 'stable'
end behaviour
from (select *, round(coalesce(revenue_change / NULLIF(previous_month_revenue, 0)*100,0)) growth_rate_perc
from cte3) t)

-- Selecting volatility based on count of growth_rate_perc
select *, case when volatility_count != 0 then 'Volatile' else 'Not Volatile' end as customer_volatility
from (select *, count(case when abs(growth_rate_perc) > 50 then 1 else null end) over(partition by customer_id) volatility_count
from cte4) t;
