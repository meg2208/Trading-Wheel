-- this holds the total benchmark value
CREATE OR REPLACE TYPE BENCHMARK_VALUES AS OBJECT (
	strategy_id NUMBER,
	contents VARRAY(10) OF BENCH_CONTENTS_TYPE,
	time DATE,
	value NUMBER,
	CONSTRUCTOR FUNCTION BENCHMARK_VALUES (VARRAY(10) 
		-- probably a syntax error here
		OF contents IN BENCH_CONTENTS_TYPE, time in DATE)
		RETURN SELF AS RESULT
	-- set up contents
);
/
CREATE OR REPLACE TYPE BODY BENCHMARK_VALUES AS
	CONSTRUCTOR FUNCTION BENCHMARK_VALUES(contents VARRAY(10) BENCH_CONTENTS_TYPE, time)
		RETURN SELF AS RESULT
		AS
		price price_curs%ROWTYPE;
		SELF.contents = contents;
		SELF.time = time;
		BEGIN
			SELF.value = 0;
			FORALL i IN contents.FIRST..CONTENTS.LAST			
				SELF.value := SELF.value + contents.get_value(SELF.time);
			RETURN
		END;
	END;
END;
/