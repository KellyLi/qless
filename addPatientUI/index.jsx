class Form extends React.Component {
  render() {
    return <form>{this.props.children}</form>;
  }
}

class Input extends React.Component {
  render() {
    return (
      <div style={{ margin: 12 }}>
        <label style={{ display: 'block' }}>{this.props.label}</label>
        <input type={this.props.type} onChange={this.onChange} />
      </div>
    );
  }

  onChange = e => {
    const target = e.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    this.props.onChange(value);
  };
}

class DateTimeInput extends React.Component {
  render() {
    return (
      <div style={{ margin: 12 }}>
        <label style={{ display: 'block' }}>{this.props.label}</label>
        <input
          type="date"
          onChange={e => this.props.onDateChange(e.target.value)}
        />
        <input
          type="time"
          onChange={e => this.props.onTimeChange(e.target.value)}
        />
      </div>
    );
  }
}

class SubmitButton extends React.Component {
  render() {
    return (
      <button type="button" onClick={this.onSubmit}>
        Submit
      </button>
    );
  }

  onSubmit = () => {
    const {
      isWalkIn,
      firstName,
      lastName,
      scheduledStartDate,
      scheduledStartTime,
    } = this.props;

    let start_date = null;
    if (!isWalkIn) {
      if (scheduledStartDate == null || scheduledStartTime == null) {
        alert('Please enter a date and time');
        return;
      }
      const time = scheduledStartTime.split(':');
      start_date = moment(scheduledStartDate)
        .hours(time[0])
        .minutes(time[1])
        .valueOf();
    }

    axios({
      method: 'post',
      url: '/checkin',
      data: {
        firstName,
        lastName,
        isWalkIn,
        scheduled_start_date: start_date,
      },
    });
  };
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isWalkIn: false,
      lastName: null,
      firstName: null,
      scheduledStartDate: null,
      scheduledStartTime: null,
    };
  }

  render() {
    return (
      <Form>
        <Input
          label="Last name"
          onChange={name => this.setState({ firstName: name })}
        />
        <Input
          label="First name"
          onChange={name => this.setState({ lastName: name })}
        />
        <Input
          label="Is Walk-in?"
          onChange={isWalkIn => this.setState({ isWalkIn: isWalkIn })}
          type="checkbox"
        />
        {!this.state.isWalkIn ? (
          <DateTimeInput
            date={this.state.scheduledStartTime}
            label="Scheduled Date"
            onDateChange={time => this.setState({ scheduledStartDate: time })}
            onTimeChange={time => this.setState({ scheduledStartTime: time })}
          />
        ) : null}
        <SubmitButton {...this.state} />
      </Form>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('form'));
