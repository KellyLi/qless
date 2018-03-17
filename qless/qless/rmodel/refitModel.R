library('forecast')
library(DBI)
library(dplyr)

load('linearRegressionModel.rda') # loads 'model' lm model
load('arimaResidualModel.rda') # loads 'fit' arima model

getDataToFit <- function() {
  conn <- dbConnect(RSQLite::SQLite(), '../database/qless.db')
  response <- dbSendQuery(
    conn,
    'SELECT * FROM qless WHERE has_been_fitted = 0 ORDER BY timestamp;'
  )
  data_to_fit <- dbFetch(response)
  
  dbClearResult(response)
  dbExecute(
    conn,
    'UPDATE qless SET has_been_fitted = 1 WHERE has_been_fitted = 0'
  )
  dbDisconnect(conn)
  
  data_to_fit
}

calcResiduals <- function(hist_df) {
  residuals <- hist_df$wait_time - hist_df$estimated_wait_time
  sign(residuals) * sqrt(abs(residuals))
}

df <- getDataToFit()
df$wait_time <- df$seen_time - df$arrival_time

if (nrow(df) > 0) {
  model <- update(model, . ~ ., data=df)
  save(model, file='linearRegressionModel-refit-test.rda')
  
  fit <- Arima(calcResiduals(df), model=fit)
  save(fit, file='arimaResidualModel-refit-test.rda')
}
