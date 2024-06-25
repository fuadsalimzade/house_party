import React, { Component }from "react";
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import { Link } from "react-router-dom";
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Radio from '@material-ui/core/Radio';
import RadioGroup from "@material-ui/core/RadioGroup";


export default class CreateRoomPage extends Component{
    defaultVotes = 2;
    API_URL = "/api"
    constructor(props) {
        super(props);
        this.state = {
            guestCanPause: true,
            votesToSkip: this.defaultVotes
        };
        this.handleGuestCanPause = this.handleGuestCanPause.bind(this);
        this.handleVotesToSkip = this.handleVotesToSkip.bind(this);
        this.handleButton = this.handleButton.bind(this);

    }
    handleGuestCanPause(e) {
        this.setState({
            guestCanPause: e.target.value === "true" ? true : false,
        });

    }
    handleVotesToSkip(e) {
        this.setState({
            votesToSkip: e.target.value,
        });

    }
    handleButton(e) {
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                votes_to_skip: this.state.votesToSkip,
                guest_can_pause: this.state.guestCanPause,
            }),
        };

        try {
            fetch(`${this.API_URL}/create`, requestOptions)
            .then((response) => response.json())
            .then((roomData) => {
                this.props.createdMessageCallBack();
                this.props.history.push("/room/" + roomData.code);
            });
        }
        catch (error) {
            console.log(error);
        }
    }

    render() {
        return (<Grid container spacing={2}>
            <Grid item xs={12} align="center">
                <Typography component='h4' variant="h4">
                    Create A Room
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText>
                        <div align="center">
                            Guest Control of Playback State
                        </div>
                    </FormHelperText>
                    <RadioGroup row defaultValue="true" onChange={this.handleGuestCanPause}>
                        <FormControlLabel 
                            value="true" 
                            control={<Radio color="primary" />}
                            label="Play/Pause"
                            labelPlacement="bottom"
                        />
                        <FormControlLabel 
                            value="false" 
                            control={<Radio color="secondary" />}
                            label="No Control"
                            labelPlacement="bottom"
                        />
                    </RadioGroup>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField 
                        required="true" 
                        type = "number" 
                        onChange={this.handleVotesToSkip}
                        defaultValue={this.defaultVotes}
                        inputProps={{
                            min: 1,
                            style: {textAlign: "center"}
                        }}
                        />
                        <FormHelperText>
                            <div align="center">
                                Votes Required To Skip Song
                            </div>
                        </FormHelperText>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" onClick={this.handleButton}>
                    Create A Room
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>)
        ;
    }
}