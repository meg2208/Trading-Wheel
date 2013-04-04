CREATE TABLE criteria (
    strategy_id INTEGER,
    indicator_id INTEGER,
    PRIMARY KEY (strategy_id, indicator_id),
    FOREIGN KEY (strategy_id) REFERENCES strategy,
    FOREIGN KEY (indicator_id) REFERENCES indicator
);
