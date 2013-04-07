CREATE TABLE portfolio_statistics (
    port_id INTEGER,
    start_date DATE,
    end_date DATE,
    sharpe_ratio REAL,
    returns REAL,
    user_id VARCHAR(20),
    PRIMARY KEY(port_id)
);
