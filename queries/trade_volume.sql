Select DISTINCT 
    S.strategy_name, 
    CS.user_id, 
    COUNT(T.trade_id)
FROM create_strategy CS, 
    action A, 
    trade T, 
    strategy S
WHERE 
    CS.strategy_id = A.strategy_id 
    AND S.strategy_id = CS.strategy_id
    AND A.trade_id = T.trade_id 
GROUP BY 
    S.strategy_name, 
    CS.user_id;
