CREATE TABLE indicator(
    indicator_id INTEGER,
    security CHAR(6),
    mva_10_day CHAR(1), -- T or F --
    mva_25_day CHAR(1), -- T or F --
    PRIMARY KEY (indicator_id)
);

