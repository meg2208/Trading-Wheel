CREATE OR REPLACE TYPE BENCHMARK_CONTENTS_TYPE AS OBJECT (
	start_date DATE,
	strategy_id NUMBER,
	security VARCHAR2(6),
	allocation NUMBER,
	shares NUMBER,
	start_value NUMBER,
	MEMBER PROCEDURE populate_shares,
	MEMBER PROCEDURE get_value(given_time DATE),
	CONSTRUCTOR FUNCTION BENCHMARK_CONTENTS_TYPE(
								strategy_id NUMBER,
								security VARCHAR2,
								allocation NUMBER)
		RETURN SELF AS RESULT
);
/
CREATE OR REPLACE TYPE BODY BENCHMARK_CONTENTS_TYPE AS
	CONSTRUCTOR FUNCTION BENCHMARK_CONTENTS_TYPE(
								strategy_id NUMBER NOT NULL, --?
								security VARCHAR2(6),
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
			RETURN
		END;
	END;
	-- fills in the correct amount of shares and start_value
	MEMBER PROCEDURE populate_shares IS	
		CURSOR price_curs(adj_close NUMBER) IS
			(SELECT DISTINCT q.adj_close
				FROM	query_data q
				WHERE	q.security = SELF.security
					AND q.time = SELF.start_date);
		CURSOR start_val_curs(start_value NUMBER) IS
			(SELECT DISTINCT s.start_value
				FROM	strategy s
				WHERE	s.strategy_id = SELF.strategy_id);
		price price_curs%ROWTYPE;
		port_val start_val_curs%ROWTYPE;
		BEGIN 
			OPEN price_curs;
			OPEN p_val_curs;
			FETCH price_curs INTO price;
			FETCH p_val_curs INTO port_val;
			SELF.shares := ROUND((port_val*SELF.allocation)/price);
			SELF.start_value := SELF.shares*price;
		END;
	END;
	-- returns total value of this security in benchmark
	MEMBER PROCEDURE get_value (given_time DATE) IS	
		CURSOR price_curs(adj_close NUMBER) IS  
			(SELECT DISTINCT q.adj_close
				FROM	query_data q
				WHERE	q.security = SELF.security
					AND q.time = given_time);
		price price_curs%ROWTYPE;
		BEGIN 
			OPEN price_curs;
			FETCH price_curs INTO price;
			RETURN price*SELF.shares;
		END;
	END;
END;
/