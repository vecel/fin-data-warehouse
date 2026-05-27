WITH source AS (
    SELECT * FROM {{ ref('wse_tickers_info') }}
),

-- quoteType,symbol,region,typeDisp,fullExchangeName,financialCurrency,,averageDailyVolume3Month,averageDailyVolume10Day,fiftyTwoWeekLowChange,fiftyTwoWeekLowChangePercent,fiftyTwoWeekRange,fiftyTwoWeekHighChange,fiftyTwoWeekHighChangePercent,fiftyTwoWeekLow,fiftyTwoWeekHigh,fiftyTwoWeekChangePercent,trailingAnnualDividendRate,trailingPE,epsTrailingTwelveMonths,fiftyDayAverage,fiftyDayAverageChange,fiftyDayAverageChangePercent,twoHundredDayAverage,twoHundredDayAverageChange,twoHundredDayAverageChangePercent,currency,firstTradeDateMilliseconds,shortName,longName,exchange,exchangeTimezoneName,exchangeTimezoneShortName,market,city,country,industry,industryKey,industryDisp,sector,sectorKey,sectorDisp,averageVolume,averageVolume10days,priceToSalesTrailing12Months,trailingAnnualDividendYield,enterpriseValue,profitMargins,heldPercentInsiders,heldPercentInstitutions,lastFiscalYearEnd,nextFiscalYearEnd,mostRecentQuarter,netIncomeToCommon,trailingEps,enterpriseToRevenue,enterpriseToEbitda,52WeekChange,SandP52WeekChange,currentPrice,recommendationKey,totalCash,totalCashPerShare,ebitda,totalDebt,quickRatio,currentRatio,totalRevenue,debtToEquity,revenuePerShare,returnOnAssets,returnOnEquity,grossProfits,freeCashflow,operatingCashflow,revenueGrowth,grossMargins,ebitdaMargins,operatingMargins,address2,compensationAsOfEpochDate,dividendRate,dividendYield,exDividendDate,fiveYearAvgDividendYield,forwardPE,floatShares,earningsQuarterlyGrowth,forwardEps,lastDividendValue,lastDividendDate,earningsGrowth,earningsTimestamp,earningsTimestampStart,earningsTimestampEnd,earningsCallTimestampStart,earningsCallTimestampEnd,isEarningsDateEstimate,epsForward,lastSplitFactor,lastSplitDate,prevName,nameChangeDate,targetHighPrice,targetLowPrice,targetMeanPrice,targetMedianPrice,numberOfAnalystOpinions,epsCurrentYear,priceEpsCurrentYear,recommendationMean,averageAnalystRating,pegRatio,irWebsite,state,auditRisk,boardRisk,compensationRisk,shareHolderRightsRisk,overallRisk,governanceEpochDate

renamed AS (
    SELECT
        CAST(symbol AS varchar(20)) AS instrument_code,

        CAST(exchange AS varchar(20)) AS exchange_code,
        CAST("fullExchangeName" AS varchar(50)) AS exchange_name,
        CAST("exchangeTimezoneShortName" AS varchar(20)) AS exchange_timezone_code,
        CAST("exchangeTimezoneName" AS varchar(50)) AS exchange_timezone_name,

        CAST(country AS varchar(50)) AS country_name,
        CAST(currency AS varchar(20)) AS currency_code
    FROM source
)

SELECT * FROM renamed