CREATE TABLE portfolio_contents (
    state_id INTEGER,
    portfolio_id INTEGER,
    security CHAR(6),
    PRIMARY KEY (state_id, portfolio_id),
    FOREIGN KEY (state_id,security) REFERENCES security_state,
    FOREIGN KEY (portfolio_id) REFERENCES aggregate_portfolio
);
