CREATE TABLE raw_data_parsing (
    strategy_id INTEGER,
    security CHAR(6),
    time DATE,
    PRIMARY KEY (strategy_id, security,time),
    FOREIGN KEY (strategy_id) REFERENCES strategy,
    FOREIGN KEY (security, time) REFERENCES query_data
);
