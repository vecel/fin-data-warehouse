-- Dimensions

CREATE TABLE DateDim (
    DateID bigint PRIMARY KEY,
    Date date,
    YearNumber bigint,
    MonthNumber bigint,
    DayNumber bigint,
    DayOfWeekNumber bigint,
    MonthName varchar(50),
    DayName varchar(50),
    IsWeekendFlag boolean,
    QuarterNumber bigint,
    IsPolandTradingDayFlag boolean,
    IsUnitedStatesTradingDayFlag boolean,
    IsUnitedStatesEarlyCloseDayFlag boolean
);

CREATE TABLE CountryDim (
    CountryID int PRIMARY KEY,
    CountryCode varchar(20),
    CountryName varchar(50),
    CurrencyCode varchar(20)
);

CREATE TABLE MacroIndicatorDim (
    IndicatorID int PRIMARY KEY,
    IndicatorCode varchar(20),
    IndicatorName varchar(100),
    Frequency varchar(20)
);

CREATE TABLE ExchangeDim (
    ExchangeID bigint PRIMARY KEY,
    ExchangeCode varchar(20),
    ExchangeName varchar(50),
    ExchangeTimeZoneCode varchar(20),
    ExchangeTimeZoneName varchar(50)
);

CREATE TABLE InstrumentDim (
    InstrumentID bigint PRIMARY KEY,
    InstrumentCode varchar(50),
    InstrumentShortName varchar(50),
    InstrumentLongName varchar(50),
    CityName varchar(50),
    StateName varchar(50),
    ZipCode varchar(20),
    InstrumentMarketName varchar(50),
    InstrumentQuoteTypeName varchar(50),
    InstrumentSectorName varchar(50),
    InstrumentIndustryName varchar(50),
    InstrumentCurrencyName varchar(50),
    InstrumentPriceCategory varchar(50),
    QuarterlyPriceChangeCategory varchar(50),
    YearlyPriceChangeCategory varchar(50),
    LastDividendDateID bigint,
    LastDividendYieldCategory varchar(50),
    ValidFromDateID bigint,
    ValidToDateID bigint,
    IsActiveFlag boolean,
    
    FOREIGN KEY (LastDividendDateID) REFERENCES DateDim(DateID),
    FOREIGN KEY (ValidFromDateID) REFERENCES DateDim(DateID),
    FOREIGN KEY (ValidToDateID) REFERENCES DateDim(DateID)
);

-- Facts

CREATE TABLE MacroFact (
    MacroFactID bigint PRIMARY KEY,
    DateID bigint,
    CountryID int,
    IndicatorID int,
    IndicatorValue double precision,
    
    FOREIGN KEY (DateID) REFERENCES DateDim(DateID),
    FOREIGN KEY (CountryID) REFERENCES CountryDim(CountryID),
    FOREIGN KEY (IndicatorID) REFERENCES MacroIndicatorDim(IndicatorID)
);

CREATE TABLE QuoteFact (
    InstrumentID bigint,
    DateID bigint,
    ExchangeID bigint,
    OpenPrice money,
    ClosePrice money,
    LowPrice money,
    HighPrice money,
    VolumeNumber bigint,
    CountryID int,
    
    PRIMARY KEY (InstrumentID, DateID),
    
    FOREIGN KEY (InstrumentID) REFERENCES InstrumentDim(InstrumentID),
    FOREIGN KEY (DateID) REFERENCES DateDim(DateID),
    FOREIGN KEY (ExchangeID) REFERENCES ExchangeDim(ExchangeID),
    FOREIGN KEY (CountryID) REFERENCES CountryDim(CountryID)
    
);

CREATE TABLE MarketNewsFact (
    MarketNewsID bigint,
    InstrumentID bigint,
    DateID bigint,
    NewsTitleName varchar(250),
    InstrumentRelevanceValue double precision,
    InstrumentSentimentValue double precision,
    InstrumentSentimentName varchar(50),
    AggregatedNewsSentimentValue double precision,
    AggregatedNewsSentimentName varchar(50),
    NewsPrimaryTopicName varchar(50),
    NewsPrimaryTopicRelevanceValue double precision,
    NewsSecondaryTopicName varchar(50),
    NewsSecondaryTopicRelevanceValue double precision,
    NewsTertiaryTopicName varchar(50),
    NewsTertiaryTopicRelevanceValue double precision,
    SourceName varchar(50),
    NewsCategoryWithinSourceName varchar(50),
    SourceLink varchar(200),
    
    PRIMARY KEY (MarketNewsID, InstrumentID),
    
    FOREIGN KEY (InstrumentID) REFERENCES InstrumentDim(InstrumentID),
    FOREIGN KEY (DateID) REFERENCES DateDim(DateID)
);
