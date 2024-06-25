import React, { Component } from "react";
import JoinRoomPage from "./JoinRoomPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import { Button, ButtonGroup, Grid, Typography } from "@material-ui/core";

export default class HomePage extends Component {
  API_URL = "/api";
  constructor(props) {
    super(props);
    this.state = {
      room_code: null,
      message: "",
    };
    this.getUserRoomInfo = this.getUserRoomInfo.bind(this);
    this.clearRoomCode = this.clearRoomCode.bind(this);
    this.createdMessage = this.createdMessage.bind(this);
    this.joinedMessage = this.joinedMessage.bind(this);
  }

  async componentDidMount() {
    this.getUserRoomInfo();
  }

  getUserRoomInfo() {
    fetch(`${this.API_URL}/check-user-room`)
      .then((response) => {
        if(response.ok) {
          return response.json();
        }
        throw new Error("User does not belong to a room");
      })
      .then((data) => {
        this.setState({
          room_code: data.room_code
        });
      })
      .catch((error) =>
        {
          console.log(error);
        });
  }

  renderHomePage() {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h3">
              House Party
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h5">
              Welcome to the home page
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <ButtonGroup variant="contained">
            <Button color="primary" to="/create" component={Link}>
              Create A Room
            </Button>
            <Button color="secondary" to="/join" component={Link}>
              Join A Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    );
  }

  clearRoomCode() {
    this.setState({
      room_code: null
    })
  }

  createdMessage() {
    this.setState({
      message: "Room created succesfully!"
    })
  }
  joinedMessage() {
    this.setState({
      message: "Joined room succesfully!"
    })
  }


  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/" render={
            () => {
              return this.state.room_code ? 
              (<Redirect to={`/room/${this.state.room_code}`} />)
               : (this.renderHomePage());
              }} 
          />
          <Route path="/join" render={
            (props) => {return <JoinRoomPage {...props} joinedMessageCallBack={this.joinedMessage} />}
          }/>
          <Route path="/create" render={
            (props) => {return <CreateRoomPage {...props} createdMessageCallBack={this.createdMessage} />}
          } />
          <Route path="/room/:roomCode" render={
            (props) => {return <Room {...props} 
                                message = {this.state.message} 
                                leaveRoomCallBack={this.clearRoomCode}/>}
          } />
        </Switch>
      </Router>
    );
  }
}