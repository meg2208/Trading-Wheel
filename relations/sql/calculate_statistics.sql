CREATE TABLE calculate_statistics (
    port_id INTEGER,
    strategy_id INTEGER,
    PRIMARY KEY (port_id),
    FOREIGN KEY (strategy_id) REFERENCES strategy,
    FOREIGN KEY (port_id) REFERENCES portfolio_statistics
);
