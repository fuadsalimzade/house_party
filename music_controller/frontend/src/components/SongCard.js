import React, { Component } from "react";
import {
  Grid,
  Typography,
  Card,
  IconButton,
  LinearProgress,
  Collapse,
} from "@material-ui/core";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import PauseIcon from "@material-ui/icons/Pause";
import SkipNextIcon from "@material-ui/icons/SkipNext";
import PlaylistPlayIcon from "@material-ui/icons/PlaylistPlay";
import Alert from "@material-ui/lab/Alert";

export default class SongCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
        message: '',
    }
  }

  skipSong() {
    fetch("/spotify/skip-song")
    .then((response) => { 
        if (!response.ok) {
            console.log(response.json());
            this.setState({
                message: "Premium account required for this feature"
            });
        }
    });
  }

  pauseSong() {
    fetch("/spotify/pause-song")
    .then((response) => { 
        if (!response.ok) {
            console.log(response.json());
            this.setState({
                message: "Premium account required for this feature"
            });
        }
    });
  }

  playSong() {
    fetch("/spotify/resume-song")
    .then((response) => { 
        if (!response.ok) {
            console.log(response.json());
            this.setState({
                message: "Premium account required for this feature"
            });
        }
    });
  }

  shuffleSong() {
    fetch("/spotify/shuffle-song")
    .then((response) => { 
        if (!response.ok) {
            console.log(response.json());
            this.setState({
                message: "Premium account required for this feature"
            });
        }
    });
  }

  render() {
    const songProgress = (this.props.progress_ms / this.props.duration_ms) * 100;

    return (
      <Card>
        <Collapse in={this.state.message} align="center">
            <Alert severity="error"  onClose={() => {
                this.setState({
                    message: "",
                })
            }}
            >
                {this.state.message}
            </Alert>
        </ Collapse>
        <Grid container alignItems="center">
          <Grid item align="center" xs={6}>
            <img src={this.props.image_cover} height="100%" width="100%" />
          </Grid>
          <Grid item align="center" xs={6}>
            <Typography component="h5" variant="h5">
              {this.props.name}
            </Typography>
            <Typography color="textSecondary" variant="subtitle1">
              {this.props.artists}
            </Typography>
            <div>
              <IconButton
                onClick={() => {
                  this.props.currently_playing ? this.pauseSong() : this.playSong();
                }}
              >
                {this.props.currently_playing ? <PauseIcon /> : <PlayArrowIcon />}
              </IconButton>
              <IconButton onClick={() => this.skipSong()}>
                {this.props.votes} / {this.props.votes_to_skip}
                <SkipNextIcon />
              </IconButton>
              <IconButton onClick={() => this.shuffleSong()}>
                <PlaylistPlayIcon />
              </IconButton>
            </div>
          </Grid>
        </Grid>
        <LinearProgress variant="determinate" value={songProgress} />
      </Card>
    );
  }
}