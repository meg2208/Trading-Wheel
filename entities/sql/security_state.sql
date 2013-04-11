CREATE TABLE security_state (
    state_id INTEGER,
    security VARCHAR2(6),
    share_amount NUMBER,
    PRIMARY KEY(state_id,security)
);
