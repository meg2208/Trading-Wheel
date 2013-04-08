CREATE TABLE trade (
    trade_id INTEGER,
    security VARCHAR2(6),
    action VARCHAR2(3),   --'B'/'S'/'X_B'/'X_U'
    share_amount NUMBER,    -- Shares purchased in this trade
    allocation NUMBER,
    price NUMBER,
    time DATE,
    PRIMARY KEY(trade_id)
);
