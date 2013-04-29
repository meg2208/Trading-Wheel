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
