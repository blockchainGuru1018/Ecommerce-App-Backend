
import axios from 'axios';
import React from 'react';

import Title from './Title';

// Generate Order Data
function createData(id, date, name, shipTo, paymentMethod, amount) {
  return { id, date, name, shipTo, paymentMethod, amount };
}

class Users extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      users: [],
      isLoading: true,
    };
  }

  componentDidMount() {
    this.setState({
      isLoading: true,
    });

    axios
      .get('/api/v1/users/1/')
      .then((res) => {
        console.log(res.data.users);
        this.setState({
          users: res.data.users,
          isLoading: false,
        })
        return true;
      })
      .catch((err) => {
        console.error(err);
        this.setState({
          isLoading: false,
        });
      });
  }

  render() {
    const { users, isLoading } = this.state;

    if (isLoading) {
      return <div>loading...</div>;
    }

    return (
      <>
        <Title>Customers</Title>
        {users.json()}
      </>
    );
  }
}

export default Users;
