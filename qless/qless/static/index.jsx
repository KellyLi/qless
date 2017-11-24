class Form extends React.Component {
  render() {
    return <form>{this.props.children}</form>;
  }
}

class Input extends React.Component {
  render() {
    return (
      <div className="form-group">
        <label>{this.props.label}</label>
        <input
          onChange={this.onChange}
          type={this.props.type}
          value={this.props.value}
        />
      </div>
    );
  }

  onChange = e => {
    const target = e.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    this.props.onChange(value);
  };
}

class DoctorDropdown extends React.Component {
  render() {
    return (
      <div className="form-group doctor-dropdown">
        <label>Doctor</label>
        <select
          className="custom-select"
          value={this.props.doctor}
          onChange={e => this.props.onChange(e.target.value)}>
          <option value="doctor_martin">Dr. Martin</option>
          <option value="doctor_hudson">Dr. Hudson</option>
        </select>
      </div>
    );
  }
}

class DateTimeInput extends React.Component {
  render() {
    return (
      <div className="form-group time-selection">
        <label>{this.props.label}</label>
        <input
          type="date"
          onChange={e => this.props.onDateChange(e.target.value)}
          value={this.props.date}
        />
        <input
          type="time"
          onChange={e => this.props.onTimeChange(e.target.value)}
          value={this.props.time}
        />
      </div>
    );
  }
}

class SubmitButton extends React.Component {
  render() {
    return (
      <button type="button" onClick={this.onSubmit}>
        Add Appointment
      </button>
    );
  }

  onSubmit = () => {
    const {
      id,
      isWalkIn,
      doctor,
      name,
      scheduledStartDate,
      scheduledStartTime,
    } = this.props;
    if (id == '' || name == '') {
      notie.alert({
        type: 'error',
        text: 'Please enter a card # and name',
        time: 2,
      });
      return;
    }

    let start_date = null;
    if (!isWalkIn) {
      if (scheduledStartDate == '' || scheduledStartTime == '') {
        notie.alert({
          type: 'error',
          text: 'Please enter a date and time',
          time: 2,
        });
        return;
      }
      const time = scheduledStartTime.split(':');
      start_date = moment(scheduledStartDate)
        .hours(time[0])
        .minutes(time[1])
        .valueOf();
    }

    if (isWalkIn) {
      let params = new URLSearchParams();
      params.append('user_id', id);
      params.append('name', name);
      axios.post('/walkin', params).then(() => {
        this.showSubmitted();
        this.props.clearForm();
      });
    } else {
      let params = new URLSearchParams();
      params.append('user_id', id);
      params.append('name', name);
      params.append('scheduled_start_time', start_date);
      params.append('doctor_name', doctor);
      axios.post('/schedule/add', params).then(() => {
        this.showSubmitted();
        this.props.clearForm();
      });
    }
  };

  showSubmitted() {
    notie.alert({
      type: 'success',
      text: 'Patient added',
    });
  }
}

class PatientTable extends React.Component {
  render() {
    const patients = this.props.patients || [];
    return (
      <table className="table">
        <thead className="thead-light">
          <tr>
            <th>Name</th>
            {this.props.isWalkIn ? null : <th>Scheduled Time</th>}
            {this.props.isPaged ? <th>Room</th> : null}
            <th />
          </tr>
        </thead>
        <tbody>
          {patients.map((patient, i) => (
            <PatientRow
              key={i}
              {...patient}
              isPaged={this.props.isPaged}
              isWalkIn={this.props.isWalkIn}
            />
          ))}
        </tbody>
      </table>
    );
  }
}

class PatientRow extends React.Component {
  render() {
    let button = null;
    if (this.props.isPaged) {
      button = (
        <button onClick={() => this.seenPatient(this.props.id)}>
          Mark Seen
        </button>
      );
    } else if (this.props.isWalkIn || this.props.is_checked_in) {
      button = (
        <select
          className="custom-select"
          onChange={e => this.pagePatient(this.props.id, e.target.value)}>
          <option value="">Page to room</option>
          <option value="Room A">A</option>
          <option value="Room B">B</option>
          <option value="Room C">C</option>
          <option value="Room D">D</option>
        </select>
      );
    } else {
      button = (
        <button onClick={() => this.checkInPatient(this.props.id)}>
          Check In
        </button>
      );
    }

    const scheduledTime = this.props.scheduled_start_time
      ? moment(this.props.scheduled_start_time).format('YYYY-MM-DD HH:mm')
      : 'N/A (Walk In)';

    return (
      <tr>
        <td>{this.props.name}</td>
        {this.props.isWalkIn ? null : <td>{scheduledTime}</td>}
        {this.props.isPaged ? <td>{this.props.room}</td> : null}
        <td>{button}</td>
      </tr>
    );
  }

  checkInPatient(id) {
    let params = new URLSearchParams();
    params.append('user_id', id);
    axios.post('/schedule/checkin', params).then(() =>
      notie.alert({
        type: 'success',
        text: 'Patient checked in',
      }),
    );
  }

  pagePatient(id, room) {
    let params = new URLSearchParams();
    params.append('user_id', id);
    params.append('room', room);
    axios.post('/page', params).then(() =>
      notie.alert({
        type: 'success',
        text: 'Patient Paged',
      }),
    );
  }

  seenPatient(id) {
    let params = new URLSearchParams();
    params.append('user_id', id);
    axios.post('/seen', params).then(() =>
      notie.alert({
        type: 'success',
        text: 'Patient marked seen',
      }),
    );
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);

    // Initialize Firebase
    var config = {
      apiKey: 'AIzaSyBqPKgj8VztRYOl6Eu42vknBHXMLFO5S7Q',
      authDomain: 'qless-74979.firebaseapp.com',
      databaseURL: 'https://qless-74979.firebaseio.com',
      projectId: 'qless-74979',
      storageBucket: 'qless-74979.appspot.com',
      messagingSenderId: '503217306609',
    };
    firebase.initializeApp(config);

    // I'm sorry
    this.state = {
      isWalkIn: false,
      name: '',
      id: '',
      scheduledStartDate: '',
      scheduledStartTime: '',
      doctor: 'doctor_martin',

      walkInPatients: [],
      doctorMartinPatients: [],
      doctorHudsonPatients: [],
      pagedPatients: [],
    };
  }

  componentDidMount() {
    const database = firebase.database();

    database.ref('/queues/walk_in/').on('value', snapshot => {
      this.setState({ walkInPatients: snapshot.val() || []});
    });
    database.ref('/queues/doctor_martin/').on('value', snapshot => {
      this.setState({ doctorMartinPatients: snapshot.val() || []});
    });
    database.ref('/queues/doctor_hudson/').on('value', snapshot => {
      this.setState({ doctorHudsonPatients: snapshot.val() || []});
    });
    database.ref('/now_paging/').on('value', snapshot => {
      this.setState({ pagedPatients: snapshot.val() || []});
    });
  }

  render() {
    return (
      <div>
        <h1>Silver Oaks Medical Clinic</h1>
        <h3>Clinic Management System</h3>
        <div className="divider"></div>
        <h2>New Appointment</h2>
        <Form>
          <div className="patient-info">
            <Input
              label="Patient Name"
              onChange={name => this.setState({ name: name })}
              value={this.state.name}
            />
            <Input
              label="Healthcard Number"
              onChange={id => this.setState({ id: id })}
              value={this.state.id}
            />
          </div>
          <Input
            label="Walk-in Patient"
            onChange={isWalkIn => this.setState({ isWalkIn: isWalkIn })}
            type="checkbox"
            value={this.state.isWalkIn}
          />
          {!this.state.isWalkIn ? (
            <DoctorDropdown
              doctor={this.state.doctor}
              onChange={doctor => this.setState({ doctor: doctor })}
            />
          ) : null}
          {!this.state.isWalkIn ? (
            <DateTimeInput
              date={this.state.scheduledStartTime}
              label="Appointment Time"
              onDateChange={time => this.setState({ scheduledStartDate: time })}
              onTimeChange={time => this.setState({ scheduledStartTime: time })}
              date={this.state.scheduledStartDate}
              time={this.state.scheduledStartTime}
            />
          ) : null}
          <SubmitButton {...this.state} clearForm={this.clearForm} />
        </Form>
        <h2>Walk In Patients</h2>
        <PatientTable patients={this.state.walkInPatients} isWalkIn={true} />
        <h2>Doctor Martin's Patients</h2>
        <PatientTable patients={this.state.doctorMartinPatients} />
        <h2>Doctor Hudson's Patients</h2>
        <PatientTable patients={this.state.doctorHudsonPatients} />
        <h2>Paging Patients</h2>
        <PatientTable patients={this.state.pagedPatients} isPaged={true} />
      </div>
    );
  }

  clearForm = () => {
    this.setState({
      name: '',
      id: '',
      scheduledStartDate: '',
      scheduledStartTime: '',
      doctor: 'doctor_martin',
    });
  };
}

ReactDOM.render(<App />, document.getElementById('root'));
