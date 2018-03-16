setwd("~/Documents/uni/FYDP/Data")
data <- read.csv(
  'fydp_data_walkin_new_queue_length_03_09_2018.csv',
  header=T
)

# Add month
data <- within(data, month <- substr(as.character(arrival_time_raw), 6, 7))
data$month <- as.integer(data$month)

# Add doctors per day
data <- within(data, date <- substr(as.character(arrival_time_raw), 1, 10))
by_day <- data %>% group_by(date)
doctors_per_day <- by_day %>% summarise(num_doctors=length(unique(doctor)))
data <- merge(data, doctors_per_day, by.x='date', by.y='date')

# add "timestamp"
data$timestamp <- data$X

# Filter out data which we don't have enough of and super long wait times
for (doc in levels(factor(data$doctor))) {
  if (nrow(subset(data, doctor == doc)) < 50) {
    data <- subset(data, doctor != doc)
  }
}
LONGEST_WAIT <- 3 * 60
data <- subset(data, wait_time < LONGEST_WAIT)
data <- subset(data, weekday != 'sun')

# get estimates
data_transformed <- within(data, wait_time <- sqrt(wait_time))
model <- lm(
  wait_time ~ queue_length + arrival_time + factor(doctor) +
    factor(num_doctors) + factor(weekday) + flow_rate + factor(month) +
    queue_length:doctor + queue_length:flow_rate + queue_length:weekday +
    queue_length:arrival_time + queue_length:factor(month) + weekday:arrival_time,
  data=data_transformed
)
predictions <- predict(model, data_transformed)^2


hist_data <- data.frame(
  arrival_time=data$arrival_time,
  weekday=data$weekday,
  flow_rate=data$flow_rate,
  queue_length=data$queue_length,
  doctor=data$doctor,
  appt_time=data$appt_time,
  is_walk_in=rep(1, nrow(data)),
  num_doctors=data$num_doctors,
  month=data$month,
  seen_time=(data$arrival_time + data$wait_time),
  estimated_wait_time=predictions,
  timestamp=data$timestamp
)

setwd('~/Documents/uni/FYDP/qless/qless/qless/database')
conn <- dbConnect(RSQLite::SQLite(), 'qless.db')
dbWriteTable(conn, 'qless', hist_data)
dbDisconnect(conn)
