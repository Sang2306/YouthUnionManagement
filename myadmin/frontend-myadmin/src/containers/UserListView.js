import React from 'react';
import Users from '../components/Users';
import axios from 'axios';
 class UserList extends React.Component{
    state = { users: [] }
    componentDidMount(){
        axios.get("myadmin/api/user")
        .then((res)=> {
            let users = res.data;
            this.setState({users})
        })
    }
     render(){
         const { users } = this.state;
         return(
            <Users data={users}/>
         );
     }
 }

 export default UserList;