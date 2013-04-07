CREATE TABLE create_strategy (
    user_id VARCHAR2(20),
    strategy_id INTEGER,
    PRIMARY KEY (user_id, strategy_id ),
    FOREIGN KEY (user_id) REFERENCES user_data,
    FOREIGN KEY (strategy_id) REFERENCES strategy
);
