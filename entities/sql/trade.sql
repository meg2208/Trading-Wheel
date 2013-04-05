CREATE TABLE trade (
    trade_id INTEGER,
    security CHAR(6),
    action CHAR(3),   --'B'/'S'/'X_B'/'X_U'
    share_amount NUMBER,    -- Shares purchased in this trade
    price NUMBER,
    time DATE,
    PRIMARY KEY(trade_id)
);
