INSERT INTO TRADE (trade_id, security, action, share_amount, allocation, price, time)
	Select seq_tid.nextval, security, buy_sell, share_amount, allocation, adj_close, time
	  FROM ( 
			SELECT q.security, ir.operator, ir.buy_sell, ir.share_amount, ir.allocation, q.adj_close, q.time, SUM(q.MVA_10_DAY) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
					AND CURRENT ROW) - q.MVA_10_DAY AS yestmva1, q.MVA_10_DAY AS mva1,
				SUM(q.MVA_25_DAY) OVER(ORDER BY q.time ROWS BETWEEN 1 PRECEDING 
					AND CURRENT ROW) - q.MVA_25_DAY AS yestmva2, q.MVA_25_DAY AS mva2
			FROM indicator L_ind, indicator R_ind, query_data q, indicator_reference ir, raw_data_parsing rd
			WHERE q.security = ir.action_security AND L_ind.MVA_10_DAY = 'T' AND R_ind.MVA_25_DAY = 'F' AND
					ir.buy_sell = 'B' AND rd.time = q.time AND ir.operator = 'x_over' 
					AND q.security = ir.action_security)
		WHERE mva1 > mva2 AND yestmva1 < yestmva2;