INSERT ALL
	INTO TRADE (trade_id, security, action, share_amount, allocation, price, time)
		VALUES(seq_tid.nextval, security, buy_sell, share_amount, allocation, adj_close, time)
	INTO MAKES_TRADE (trade_id, portfolio_id)
		VALUES(seq_tid.currval, portfolio_id)
SELECT portfolio_id, a.security, a.buy_sell, a.share_amount, a.allocation, a.adj_close, a.time
	FROM ( 
		SELECT rd.strategy_id, q.security, ir.operator, ir.buy_sell, ir.share_amount, ir.allocation, 
				q.adj_close, q.time, 
				SUM(q.MVA_10_DAY) OVER(ORDER BY q.security, q.time ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) - q.MVA_10_DAY AS yestmva1, 
			   	q.MVA_10_DAY AS mva1,
				SUM(q.MVA_25_DAY) OVER(ORDER BY q.security, q.time ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) - q.MVA_25_DAY AS yestmva2, 
				q.MVA_25_DAY AS mva2
		FROM indicator L_ind, query_data q, indicator_reference ir, raw_data_parsing rd,
				criteria c
		WHERE q.security = ir.action_security 
			AND rd.security = ir.action_security
			AND L_ind.indicator_id = ir.L_indicator_id
			AND L_ind.MVA_10_DAY = 'T'
			AND ir.R_indicator_id = c.indicator_id
			AND c.strategy_id = {0}
			AND rd.time = q.time 
			AND ir.operator = 'x_over' 
			AND q.security = ir.action_security
			AND rd.strategy_id = {0}) a,
  	  (SELECT ag.portfolio_id, ag.time, dtd.strategy_id
  			FROM aggregate_portfolio ag, day_to_day dtd
  			WHERE ag.time = time
  				AND ag.portfolio_id = dtd.portfolio_id
  				AND dtd.strategy_id = {0}) b
	WHERE a.mva1 > a.mva2 
	  AND a.yestmva1 < a.yestmva2
	  AND b.time = a.time