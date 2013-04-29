CREATE OR REPLACE TYPE BENCHMARK_CONTENTS_TYPE AS OBJECT (
	start_date DATE,
	strategy_id NUMBER,
	security VARCHAR2(6),
	allocation NUMBER,
	shares NUMBER,
	start_value NUMBER,
	MEMBER PROCEDURE populate_shares,
	MEMBER FUNCTION get_value(given_time DATE)
		RETURN NUMBER,
	MEMBER FUNCTION multiply(num1 NUMBER, num2 NUMBER)
		RETURN NUMBER,
	MEMBER FUNCTION divide(num1 NUMBER, num2 NUMBER)
		RETURN NUMBER,
	CONSTRUCTOR FUNCTION BENCHMARK_CONTENTS_TYPE(
								strategy_id NUMBER,
								security VARCHAR2,
								allocation NUMBER)
		RETURN SELF AS RESULT
);
/
CREATE OR REPLACE TYPE BODY BENCHMARK_CONTENTS_TYPE AS
	CONSTRUCTOR FUNCTION BENCHMARK_CONTENTS_TYPE(
								strategy_id NUMBER,
								security VARCHAR2,
								allocation NUMBER)
	RETURN SELF AS RESULT
	AS
	BEGIN
		--sets start_date attribute
			SELECT 	MIN(time) 
			INTO SELF.start_date
			FROM	raw_data_parsing
			WHERE	strategy_id = SELF.strategy_id;
		populate_shares(); -- sets share amount for this security
		RETURN;
	END;
		
	MEMBER FUNCTION multiply (num1 NUMBER, num2 NUMBER) RETURN NUMBER IS
	BEGIN
		RETURN num1 * num2;
	END multiply;

	MEMBER FUNCTION divide (num1 NUMBER, num2 NUMBER) RETURN NUMBER IS
	BEGIN
		RETURN num1 / num2;
	END divide;

	-- fills in the correct amount of shares and start_value
	MEMBER PROCEDURE populate_shares IS	
		CURSOR price_curs IS
			(SELECT DISTINCT q.adj_close
				FROM	query_data q
				WHERE	q.security = SELF.security
					AND q.time = SELF.start_date);
		CURSOR start_val_curs IS
			(SELECT DISTINCT s.start_value
				FROM	strategy s
				WHERE	s.strategy_id = SELF.strategy_id);
		price NUMBER;
		port_val NUMBER;
	BEGIN 
		OPEN price_curs;
		OPEN start_val_curs;
		FETCH price_curs INTO price;
		FETCH start_val_curs INTO port_val;
		SELF.shares := multiply(port_val, SELF.allocation);
		SELF.shares := FLOOR(divide(SELF.shares, price));
		SELF.start_value := multiply(SELF.shares, price);
        COMMIT;
	END populate_shares;

    -- returns total value of this security in benchmark
	MEMBER FUNCTION get_value (given_time DATE) RETURN NUMBER IS	
		CURSOR price_curs IS  
			(SELECT DISTINCT q.adj_close
				FROM	query_data q
				WHERE	q.security = SELF.security
					AND q.time = given_time);
		price NUMBER;
		temp_value NUMBER;
	BEGIN 
		OPEN price_curs;
		FETCH price_curs INTO price;
		temp_value := multiply(price,SELF.shares);
		RETURN temp_value;
	END get_value;
END;
/
