CREATE TABLE security_state (
    state_id INTEGER,
    security CHAR(6),
    security_price NUMBER,
    share_amount NUMBER,
    PRIMARY KEY(state_id,security)
);
