-- finds all buy/sell signals for a given strategy_id
-- each row reads out like a sentence of how the orders are triggered
SELECT L_ind.MVA_10_DAY, L_ind.MVA_25_DAY, L_ind.security, ind_ref.operater, 
		R_ind.MVA_10_DAY, R_ind.MVA_25_DAY, R_ind.security, ind_ref.buy_sell,
		ind_ref.share_amount, ind_ref.allocation, ind_ref.action_security,
		ind_ref.cash_value
	FROM 
		ind_ref indicator_reference, L_ind indicator, 
			R_ind indicator, criteria
	WHERE
		ind_ref.L_indicator_id = L_ind.indicator_id AND
		ind_ref.R_indicator_id = R_ind.indicator_id AND
		criteria.strategy_id = {0}