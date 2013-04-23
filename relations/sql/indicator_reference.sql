CREATE TABLE indicator_reference(
    start_time DATE,    -- DD-MMM-YYYY
    end_time DATE,      -- DD-MMM-YYYY
    L_indicator_id INTEGER,
    R_indicator_id INTEGER,
    buy_sell CHAR(1),   --'B' or 'S'
    operator VARCHAR2(10),
    action_security VARCHAR2(6),
    share_amount INTEGER,   --NULL
    allocation NUMBER,      --100
    cash_value NUMBER, -- Starting cash amt
    PRIMARY KEY (L_indicator_id,R_indicator_id,buy_sell, action_security),
    FOREIGN KEY (L_indicator_id) REFERENCES indicator,
    FOREIGN KEY (R_indicator_id) REFERENCES indicator
);
