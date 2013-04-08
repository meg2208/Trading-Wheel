CREATE TABLE indicator(
    indicator_id INTEGER,
    security VARCHAR2(6),
    mva_10_day VARCHAR2(1), -- T or F --
    mva_25_day VARCHAR2(1), -- T or F --
    PRIMARY KEY (indicator_id)
);
