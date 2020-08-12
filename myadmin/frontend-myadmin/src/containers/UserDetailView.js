import React from 'react';
import axios from 'axios';
import User from '../components/User';


 class UserDetail extends React.Component{
    state = { user: {} }
    componentDidMount(){
        const userID = this.props.match.params.user_ID;
        axios.get(`myadmin/api/user/${userID}`)
        .then((res)=> {
            this.setState({user: res.data})
        })
    }
    render(){
        const user = this.state;
        return(
            <User data={user}/>
        );
    }
    
    }

 export default UserDetail;