-- customers with orders with quantities > 5 with their company names

-- drops
drop table order_greater_5;
drop table projected_orders;

-- step 1
DECLARE
BEGIN
	ops.go(
		ops.filter_ra('product_order', 'quantity>5', 'order_greater_5')
	);
END;
/

-- step 2
DECLARE
BEGIN
	ops.go(
		ops.reduce_ra('order_greater_5', 'cust_id, order_id', 'cid_order_greater_5')
	);
END;
/

DECLARE
BEGIN
	ops.go(
		ops.mjoin_ra('cid_order_greater_5', 'cust_id' 'cust_id', 'cust_id', 'cid_order_greater_5')
	);
END;
/




----- examples

drop table cust_w_m17;

DECLARE
BEGIN
	ops.go(
		ops.filter_ra('product_order', 'product_id="m17"', 'cust w m17')
	);
END;
/


DECLARE
BEGIN
	ops.go(
		ops.filter_ra('product_order', 'quantity=10', 'cust w m17')
	);
END;
/

DECLARE
BEGIN
	ops.go(
		ops.filter_ra('product_order', 'o_status=O', 'cust w m17')
	);
END;
/


DECLARE
BEGIN
	ops.go(
		ops.filter_ra('customer', 'company_name="ABESTOS, INC."', 'cust w m17')
	);
END;
/

DECLARE
BEGIN
	ops.go(
		ops.reduce_ra('product_order', 'cust_id, order_id, quantity', 'projected orders')
	);
END;
/

