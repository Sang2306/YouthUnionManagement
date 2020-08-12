import React from 'react';
import { Button, Tooltip } from 'antd';
import { Table } from 'reactstrap';
import {DeleteOutlined, EditOutlined} from '@ant-design/icons';
const User = (props) => {
    const {user} = props.data;
    return(
    <Table>
    <thead>
        <tr>
            <th>Sinh viên ID</th>
            <th>Class ID</th>
            <th>Tên sinh viên</th>
            <th>Vai trò</th>
            <th>Mật Khẩu</th>
            <th>Điểm chuyên cần</th>
        </tr>
    </thead>
    <tbody>
       <tr key={user.user_ID}>
       <td>{user.user_ID}</td>
       <td>{user.class_ID}</td>
       <td>{user.name}</td>
       <td>{user.role}</td>
       <td>{user.password}</td>
        <td>{user.accumulated_point}</td>
       <td>
       <Tooltip placement="leftBottom" title={<span>Delete</span>}>
           <Button type="danger" size="smail"><DeleteOutlined /></Button>
           </Tooltip>
           <Tooltip placement="rightBottom" title={<span>Edit</span>}>
           <Button type="primary" size="smail"><EditOutlined /></Button>
      </Tooltip>
       </td>
   </tr>
    </tbody>

    </Table>  
    
    );
}

export default User;