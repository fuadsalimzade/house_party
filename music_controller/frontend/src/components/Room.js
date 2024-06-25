import React, {Component} from "react";
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
import { ButtonGroup, Collapse } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import SongCard from "./SongCard";


export default class Room extends Component {
    API_URL = "/api/room/?roomCode="
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            message: this.props.message.toString() || "",
            settings: false,
            updateClicked: false,
            alertColapse: true,
            roomEntry: true,
            spotifyAuthenticated: false,
            song: {},
        }
        this.roomCode = this.props.match.params.roomCode;
        this.getRoomDetails = this.getRoomDetails.bind(this);
        this.handleButton = this.handleButton.bind(this);
        this.handleUpdateButton = this.handleUpdateButton.bind(this);
        this.updateRoomSettings = this.updateRoomSettings.bind(this);
        this.handleGuestCanPause = this.handleGuestCanPause.bind(this);
        this.handleVotesToSkip = this.handleVotesToSkip.bind(this);
        this.handleSettingButton = this.handleSettingButton.bind(this);
        this.authenticateSpotify = this.authenticateSpotify.bind(this);
        this.getCurrentSong = this.getCurrentSong.bind(this);
        this.getRoomDetails();
    }
    componentDidMount() {
        this.song_interval = setInterval(this.getCurrentSong, 1000);
        this.room_interval = setInterval(this.getRoomDetails, 1000);
    }
    componentWillUnmount() {
        clearInterval(this.song_interval);
        clearInterval(this.room_interval);
    }

    getCurrentSong() {
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include" 
        };
        fetch(`/spotify/current-song`, requestOptions)
        .then((response) => {
            if (!response.ok){
                console.log(response)
                return {};
            } else {
                return response.json();
            }
        })
        .then((data) => this.setState({
            song: data,
        }))
    }

    authenticateSpotify() {
        fetch(`/spotify/check-user-authentication`)
        .then((response) => response.json())
        .then((data) => {
            this.setState({
                spotifyAuthenticated: data.status,
            });
            if (!data.status) {
                fetch(`/spotify/get-auth-url`)
                .then((response) => response.json())
                .then((data) => {
                    window.location.replace(data.url);
                })
            }
        })
    }
    
    handleButton() {
        const requestOptions = {
            method : "POST",
            headers: {
                "Content-Type": "application/json",
            },
        }
        fetch(`/api/leave-room`, requestOptions)
        .then((_response) =>{
            this.props.leaveRoomCallBack();
            this.props.history.push("/");
        });
    }

    getRoomDetails() {
        fetch(`${this.API_URL}${this.roomCode}`)
            .then((response) => {
                if (!response.ok) {
                    this.props.leaveRoomCallBack();
                    this.props.history.push("/");
                }
                return response.json();
            })
            .then((data) => {
                this.setState({
                    votesToSkip: data.votes_to_skip,
                    guestCanPause: data.guest_can_pause,
                    isHost: data.host,
                });
                if (this.state.isHost) {
                    this.authenticateSpotify();
                }
            });
    }

    handleUpdateButton() {
        const requestOptions = {
            method : "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "code": this.roomCode,
                "guest_can_pause": this.state.guestCanPause,
                "votes_to_skip": this.state.votesToSkip
            })
        }
        fetch(`/api/update-room`, requestOptions)
        .then((response) => response.json())
        .then((data) => {
            // Handle the response data if needed
            console.log(data);
            this.setState({
                message: "Room settings have been updated successfully.",
                updateClicked: true,
            })
        })
    }
    handleGuestCanPause(e) {
        this.setState({
            guestCanPause: e.target.value === "true" ? true : false
        });
    }
    handleVotesToSkip(e) {
        this.setState({
            votesToSkip: e.target.value
        });
    }
    handleSettingButton() {
        if (this.state.settings) {
            this.setState({
                settings: false,
                alertColapse: true,
                roomEntry: false,
            })
        } else {
            this.setState({
                settings: true,
                updateClicked: false,
            })
        }

    }

    updateRoomSettings() {
        return (<Grid container spacing={2}>
            <Grid item xs={12} align="center">
                <Typography component='h4' variant="h4">
                    Update Room Settings
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Collapse in={this.state.alertColapse}>
                    {this.state.updateClicked ? (
                        <Alert severity="success"  onClose={() => {
                            this.setState({
                                message: "",
                                alertColapse: false
                            })
                        }}
                        >
                            {this.state.message}
                        </Alert>
                    ) : null }
                </Collapse>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText>
                        <div align="center">
                            Guest Control of Playback State
                        </div>
                    </FormHelperText>
                    <RadioGroup row defaultValue={this.state.guestCanPause.toString()} onChange={this.handleGuestCanPause}>
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
                        defaultValue={this.state.votesToSkip}
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
                <Button color="primary" 
                        variant="contained" 
                        onClick={this.handleUpdateButton} 
                        disabled={this.state.updateClicked}>
                    Update
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" onClick={this.handleSettingButton}>
                    Back
                </Button>
            </Grid>
        </Grid>
        );
    }

    render() {
        if (this.state.settings) {
            return this.updateRoomSettings();
        }
        else {
            return (
                    <Grid container spacing={2}>
                        <Grid item xs={12} align="center">
                            <Collapse in={this.state.roomEntry}>
                                <Alert severity="success"  onClose={() => {
                                    this.setState({
                                        message: "",
                                        roomEntry: false,
                                    })
                                }}
                                >
                                    {this.state.message}
                                </Alert>
                            </Collapse>
                        </Grid>
                        <Grid item xs={12} align="center">
                            <Typography variant="h5" component="h5">
                                Room Code: {this.roomCode}
                            </Typography>
                        </Grid>
                        <SongCard {...this.state} />
                        <Grid item xs={12} align="center">
                            <ButtonGroup variant="contained" >
                                <Button color="secondary" onClick={this.handleButton}>
                                    Leave Room
                                </Button>
                                { this.state.isHost ? (
                                <Button color="primary" onClick={this.handleSettingButton}>
                                    Settings
                                </Button>
                                ) : null}
                            </ButtonGroup>
                        </Grid>
                    </Grid>
            );
        }
    }
}