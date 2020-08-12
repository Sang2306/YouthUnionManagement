import React from 'react';
import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';


class CreateUser extends React.Component{
    constructor(props){
        super (props);
        this.state ={
            data: {}
        };
    }
    handleSubmit = event => {

    };
    handleChange = event => {

    };
    render(){
        return(
        <Form>
            <FormGroup>
                <Label for="user_ID">Sinh viên ID</Label>
                <Input type="text" name="email" id="user_ID" placeholder="Nhập ID" />
            </FormGroup>
            <FormGroup>
                <Label for="class_ID">Lớp ID</Label>
                <Input type="text" name="" id="class_ID" placeholder="Nhập lớp ID" />
            </FormGroup>
            <FormGroup>
                <Label for="name"></Label>
                <Input type="text" name="name" id="name" placeholder="Nhập tên" />
            </FormGroup>
            <FormGroup>
                <Label for="password">Password</Label>
                <Input type="password" name="password" id="password" placeholder="Nhập mật khẩu" />
            </FormGroup>
            <FormGroup>
                <Label for="role">Email</Label>
                <Input type="" name="role" id="role" placeholder="with a placeholder" />
            </FormGroup>
            <FormGroup>
                <Label for="exampleEmail">Email</Label>
                <Input type="email" name="email" id="exampleEmail" placeholder="with a placeholder" />
            </FormGroup>
            <Button>Submit</Button>
        </Form>
        );
    }
}
