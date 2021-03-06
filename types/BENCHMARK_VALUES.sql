-- this holds the total benchmark value
CREATE OR REPLACE TYPE BENCHMARK_VALUES AS OBJECT (
	strategy_id NUMBER,
	contents CONTENTS_LIST,
	time DATE,
	value NUMBER,
    MEMBER FUNCTION add_it (num1 NUMBER, num2 NUMBER)
        RETURN NUMBER,
    MEMBER FUNCTION calculate_value(contents CONTENTS_LIST)
	CONSTRUCTOR FUNCTION BENCHMARK_VALUES (contents CONTENTS_LIST, time DATE) 
        RETURN SELF AS RESULT
);
/
CREATE OR REPLACE TYPE BODY BENCHMARK_VALUES AS
	CONSTRUCTOR FUNCTION BENCHMARK_VALUES(contents CONTENTS_LIST, time DATE)
		RETURN SELF AS RESULT
		AS
            pragma autonomous_transaction;
            temp NUMBER;
		BEGIN
            SELF.contents := contents;
		    SELF.time := time;
			SELF.value := 0;

			FOR i IN SELF.contents.FIRST..SELF.contents.LAST LOOP
                temp := SELF.contents(i).get_value(SELF.time);
				SELF.value := add_it(SELF.value, temp);
            END LOOP;
			RETURN;
	    END;

	MEMBER FUNCTION calculate_value()

    MEMBER FUNCTION add_it (num1 NUMBER, num2 NUMBER) RETURN NUMBER IS
	    BEGIN
	        RETURN num1 + num2;
	    END add_it;
END;
/
