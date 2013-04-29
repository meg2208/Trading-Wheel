-- this populates the portfolio_value and risk_free_rate
-- in the analysis table
CREATE OR REPLACE TYPE HELPER AS OBJECT (
	analysis_id NUMBER,
	time DATE,
	strategy_id NUMBER,
	--frequency VARCHAR2(10), -- daily, monthly, yearly, overall
	MEMBER PROCEDURE set_rf_pv,
    CONSTRUCTOR FUNCTION HELPER (time DATE, strategy_id NUMBER,
								analysis_id NUMBER)
	RETURN SELF AS RESULT
);
/
CREATE OR REPLACE TYPE BODY HELPER AS
	CONSTRUCTOR FUNCTION HELPER(time DATE, strategy_id NUMBER, 
								analysis_id NUMBER)
		RETURN SELF AS RESULT
	AS
	BEGIN
		SELF.time := time;
		SELF.strategy_id :=strategy_id;
		set_rf_pv();
	END;

	-- sets the risk-free rate and portfolio value
	-- for the analysis on the given date
	MEMBER PROCEDURE set_rf_pv IS	
	BEGIN 
	UPDATE analysis a
		SET a.portfolio_value = (
				SELECT ag.portfolio_value
				FROM aggregate_portfolio ag,
						day_to_day dtd 
				WHERE ag.portfolio_id = dtd.portfolio_id
					AND ag.time = SELF.time
					AND dtd.strategy_id = SELF.strategy_id
				)
			WHERE a.analysis_id = SELF.analysis_id;
	COMMIT;
	UPDATE analysis a
		SET a.risk_free_rate = (
				SELECT (q.adj_close/100)/365
				FROM query_data q, raw_data_parsing rd
				WHERE q.time = rd.time
				AND 	q.security = '^IRX'
				AND 	rd.strategy_id = SELF.strategy_id
				)
			WHERE a.analysis_id = SELF.analysis_id;
	COMMIT;
	END;
END;
/
