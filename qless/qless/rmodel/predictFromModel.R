LAMBDA <- 0.31
inverseBoxcoxTransform <- function(y, lambda = LAMBDA) {
  if (lambda < 0.05 && lambda > -0.05) {
    10^y
  } else {
    (y * lambda + 1)^(1/lambda)
  }
}

args <- commandArgs(TRUE)
arrival <- as.double(args[1])
weekday <- as.character(args[2])
flow <- as.double(args[3])
queue <- as.double(args[4])
doctor <- as.character(args[5])
appointment <- as.double(args[6])
isWalkIn <- as.integer(args[7])

print(isWalkIn)
if (isWalkIn == 1) {
  modelName <- 'walkInModel.rda' 
} else {
  modelName <- 'scheduledModel.rda'
}
load(modelName)

estimateWaitTime = function(
  arrival_time, weekday, flow_rate, queue_length, doctor, appointment_time
) {
  df = data.frame(
    arrival_time=arrival_time,
    weekday=weekday,
    flow_rate=flow_rate,
    queue_length=queue_length,
    doctor=doctor,
    appointment_time=appointment_time
  )
  pred = predict(model, newdata=df)
  pred[pred < 0] <- 0
  inverseBoxcoxTransform(pred)
  pred[[1]]
}

estimateWaitTime(arrival, weekday, flow, queue, doctor, appointment)

