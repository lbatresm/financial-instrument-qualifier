# FINANCIAL INSTRUMENT QUALIFIER

The aim of this software is to quantitatively evaluate personal investment porfolios (commonly known as Portfolio Management). Taking into account the information that the user provides (assets, risk tolerance, diversification preferences...) and gathering information from diferent data sources, we can give the user valuable advice.

This repo comprises a set of tools to be used together with agentic AI infrastructures to get the best possible user experience. 

## WHAT WOULD WE LIKE TO MEASURE?





## OUR TOOLS
### Why Open FIGI?
OpenFIGI is Bloomberg's public API that provides access to the global database of FIGI (Financial Instrument Global Identifier) ​​identifiers.
Its mission is to unify financial instrument identifiers (stocks, bonds, ETFs, funds, derivatives, indices, etc.) through a unique, standardized ID.

Each instrument has a FIGI (for example: BBG000B9XRY4 for AAPL US Equity).

Since each data source in the internet can use a different identifier for financial instruments (ISIN, Ticker, CUSIP, SEDOL...), the Financial Instrument Global Identifier allows us to correlate them and avoid dupplications in our system.

### Why yfinance API?

Yahoo Finance provides comprehensive financial data through the yfinance API, offering rich information about funds, ETFs, and other financial instruments beyond just identifiers. 

It provides detailed fund characteristics such as asset class composition, top holdings, bond and equity holdings breakdowns, sector weightings, credit ratings, and fund operations. 
