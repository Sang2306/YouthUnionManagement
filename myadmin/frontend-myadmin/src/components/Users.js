import React from  'react';
import { Button, Tooltip } from 'antd';
import { Table } from 'reactstrap';
import { Link } from 'react-router-dom';

const Users = (props) => {
    return (
        <Table>
        
        <thead>
            <tr>
                <th>Sinh viên ID</th>
                <th>Tên sinh viên</th>
                <th>Mật Khẩu</th>
            </tr>
        </thead>
    
        <tbody>
       {props.data.map((user)=>(
           <tr key={user.user_ID}>
           <td>{user.user_ID}</td>
           <td>{user.name}</td>
            <td>{user.password}</td>
           <td>
           <Tooltip placement="rightBottom" title={<span>Detail</span>}>
            <Link to={`/${user.user_ID}`}>
            <Button type="primary" ghost>Detail</Button>
            </Link>
            </Tooltip>
           </td>

       </tr>
       ))}
        
        </tbody>
    
    </Table>  
    );
}

export default Users;