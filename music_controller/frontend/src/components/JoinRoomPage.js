import React, { Component }from "react";
import { Grid, Button, Typography, TextField, FormHelperText } from "@material-ui/core";
import { Link } from "react-router-dom";


export default class JoinRoomPage extends Component{
    API_URL = "/api/room/?roomCode="
    constructor(props) {
        super(props);
        this.state = {
            code: "",
            error: "",
        };

        this.handleButton = this.handleButton.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleButton() {
        if (this.state.code === "") {
            this.setState({
                error: "Code cannot be an empty string"
            });
        } else {
            this.setState({
                error: ""
            });
        }
        try{
            fetch(`${this.API_URL}${this.state.code}`)
            .then((response)=>{
                if (response.ok) 
                    {
                        this.props.joinedMessageCallBack();
                        this.props.history.push(`/room/${this.state.code}`);
                    }
                else {
                    this.setState({
                        error: "Room not found"
                    });
                }
            })
        } catch(error) {
            this.setState({
                error: error
            });
        }
    }

    handleChange(e) {
        this.setState({
            code: e.target.value
        });
    }

    render() {
        return (
        <Grid container spacing={2}>
            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    <div>
                        Join The Room
                    </div>
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <TextField 
                    required="true"
                    value={this.state.code} 
                    error = {this.state.error}
                    label="Code"
                    placeholder="Enter a Room Code"
                    helperText={this.state.error}
                    onChange={this.handleChange} />
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" onClick={this.handleButton}>
                    Join The Room
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
        
        )
    }
}