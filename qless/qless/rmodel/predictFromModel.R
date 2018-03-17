library('forecast')
library(DBI)
library(dplyr)

args <- commandArgs(TRUE)
arrival <- as.integer(args[1])
weekday <- as.character(args[2])
flow <- as.integer(args[3])
queue <- as.integer(args[4])
doctor <- as.integer(args[5])
appointment <- as.integer(args[6])
isWalkIn <- as.integer(args[7])
num_doctors <- as.integer(args[8])
month <- as.integer(args[9])

load('linearRegressionModel.rda') # loads 'model' lm model
load('arimaResidualModel.rda') # loads 'fit' arima model

linearRegressionPredict <- function(predictors) {
  pred <- predict(model, predictors, interval='predict', level=0.95)
  pred[pred < 0] <- 0
  lwr <- pred[1, 2]
  upr <- pred[1, 3]
  avg <- pred[1, 1]
  c(lwr, upr, avg)
}

arimaPredict <- function(history, forecast_distance) {
  refit <- Arima(history, model=fit)
  fcast <- forecast(refit, h=forecast_distance)
  last(fcast$mean)
}

getHistoricResiduals <- function() {
  conn <- dbConnect(RSQLite::SQLite(), '../database/qless.db')
  response <- dbSendQuery(
    conn,
    'SELECT * FROM qless ORDER BY timestamp DESC LIMIT 15;'
  )
  hist_df <- dbFetch(response)
  dbClearResult(response)
  dbDisconnect(conn)

  # Calculate residuals
  wait_time <- hist_df$seen_time - hist_df$arrival_time
  residuals <- wait_time - hist_df$estimated_wait_time
  sign(residuals) * sqrt(abs(residuals))
}

transformPredictionToMinutes <- function(prediction) {
  prediction^2
}

roundToNearestFive <- function(n) {
  round(n / 5)* 5
}

estimateWaitTime = function(
  arrival_time, weekday, flow_rate, queue_length, doctor,
  appointment_time, num_doctors, month
) {
  df <- data.frame(
    arrival_time=arrival_time,
    weekday=weekday,
    flow_rate=flow_rate,
    queue_length=queue_length,
    doctor=doctor,
    appointment_time=appointment_time,
    num_doctors=num_doctors,
    month=month
  )

  historic_residuals <- getHistoricResiduals();
  if (length(historic_residuals) < 15) {
    historic_residuals <- append(rep(0, 15 - length(historic_residuals)),
                                  historic_residuals)
  }
 
  lr_prediction <- linearRegressionPredict(df)
  arima_correction <- if (queue_length > 0) {
    arimaPredict(historic_residuals, queue_length)
  } else {
    0
  }
  prediction <- lr_prediction + arima_correction
  roundToNearestFive(transformPredictionToMinutes(prediction))
}

estimateWaitTime(arrival, weekday, flow, queue, doctor, appointment,
                 num_doctors, month)

