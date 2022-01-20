import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import TravelExploreIcon from '@mui/icons-material/TravelExplore';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import TextField from '@mui/material/TextField';
import ListItemText from '@mui/material/ListItemText';
import {createTheme, ThemeProvider} from '@mui/material/styles';

import $ from 'jquery'; 
import {useState, useEffect} from "react";
import {initializeApp} from 'firebase/app';
import {getAuth, onAuthStateChanged, GoogleAuthProvider, signInWithPopup, signOut} from 'firebase/auth';
import {getFirestore, collection, onSnapshot, addDoc} from 'firebase/firestore';

require('dotenv').config()

const firebaseConfig = require(`../FirebaseConfigs/firestore.json`);
const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);
const theme = createTheme({
  typography: {
    fontSize: 14,
    fontFamily: [
        'Roboto'
    ].join(','),
  },
});


console.log('ENV:' , process.env)

export default function Website() {
    // Global variables
    const currentTime = new Date().toISOString();  // UTC
    const WRITE_SERVER_IP = process.env.REACT_APP_WRITE_SERVER_IP;
    const READ_SERVER_IP = process.env.REACT_APP_READ_SERVER_IP;

    // Global hooks:
    const [records, setRecords] = useState([]);
    const [sumOfAges, setSumOfAges] = useState(0);

    // Global effects
    useEffect(() => listenToRecords(), []);

    function Copyright() {
        return (
            <Typography variant="body2" color="text.secondary" align="center">
                {'© '} {new Date().getFullYear()} {' '}
                <Link color="inherit" href="https://youtu.be/dQw4w9WgXcQ">
                     Dawid Dieu
                </Link>{' '}
                {'All right reserved.'}
            </Typography>
        );
    }


    function listenToRecords() {
        return fetch(READ_SERVER_IP)
        .then((response) => response.json())
        .then((responseJson) => {
            setRecords(responseJson['users_list'].map(
                (user, index) => ({
                    id: index,
                    data: user,
                })
            ));
            setSumOfAges(responseJson['stats']['sum_of_ages']);
            // console.log(responseJson)
        })
        .catch((error) => {
            console.error(error);
        });
     }


    //  Firebase database
    // const listenToRecords = () => {
    //     getMoviesFromApiAsync()
    //     const firestore = getFirestore(firebaseApp);
    //     const recordsCol = collection(firestore, 'clouds-website')
      
    //     let unsubscribe = onSnapshot(recordsCol, (recordsSnapshot) => {
    //         setRecords(recordsSnapshot.docs.map(
    //             snap => ({
    //                 id: snap.id,
    //                 data: snap.data(),
    //             })
    //         ));
    //     });
    //     return () => {
    //         console.log("Stopped listening.");
    //         unsubscribe();
    //     };
    //   }
    
    const Form = () => {
        const [nick, setNick] = useState('');
        const [name, setName] = useState('');
        const [surname, setSurname] = useState('');
        const [age, setAge] = useState('');

        const handleClck = async (event) => {
            // Saving to Firestore
            // const firestore = getFirestore(firebaseApp);
            // const recordsCol = collection(firestore, 'clouds-website')

            // const docRef = await addDoc(recordsCol, {
            //     nick: nick,
            //     name: name,
            //     surname: surname,
            //     age: age
            // });
            // console.log("Document written with ID: ", docRef.id);

            fetch(WRITE_SERVER_IP, {
                method: 'POST',
                headers: new Headers(),
                body: JSON.stringify({ 
                    nick: nick,
                    name: name,
                    surname: surname,
                    age: age
                })
            }).then((res) => res.json())
                .then((data) => console.log(data))
                .catch((err) => console.log(err))

            window.location.reload(false);
        };


        return (
            <Box
                component="form"
                sx={{'& .MuiTextField-root': { m: 1, width: '25ch' },}}
                noValidate
                autoComplete="off"
            >
                <Box textAlign='center'>
                    <TextField id="outlined-basic" label="Nickname" variant="outlined" value={nick} onChange={(e) => setNick(e.target.value)}/>
                    <TextField id="outlined-basic" label="Name" variant="outlined" value={name} onChange={(e) => setName(e.target.value)}/>
                    <TextField id="outlined-basic" label="Surname" variant="outlined" value={surname} onChange={(e) => setSurname(e.target.value)} />
                    <TextField id="outlined-basic" label="Age" variant="outlined" value={age} onChange={(e) => setAge(e.target.value)}/>
                    {/* <TextField id="outlined-basic" label="Height" variant="outlined" />
                    <TextField id="outlined-basic" label="Weight" variant="outlined" />
                    <TextField id="outlined-basic" label="Gender" variant="outlined" /> */}
                </Box>
                
                <Box mt="30px" textAlign='center'>
                    <Button variant="contained" color="success" onClick={handleClck}>
                        Send Data
                    </Button>
                </Box>
            </Box>
        );
    }


    const RecordsGrid = () => {
        return (
            <Grid container spacing={1}>
                {records.map((record) => (
                    <Grid item key={record.id} xs={12} sm={6} md={4}>
                        <Card
                            sx={{
                                height: '100%', display: 'flex', flexDirection: 'column',
                                backgroundColor: "#89c4f4"}
                            }
                        >
                            <CardContent sx={{flexGrow: 1}}>
                                <List dense={false} disablePadding>
                                    <ListItem disablePadding>
                                        <ListItemText
                                            primary={"Nickname: " + record.data.nick}
                                            secondary={
                                                <List>
                                                    <ListItem>{"Name: " + record.data.name}</ListItem>
                                                    <ListItem>{"Surname: " + record.data.surname}</ListItem>
                                                    <ListItem>{"Age: " + record.data.age}</ListItem>
                                                    <ListItem>{"New Nickname: " + record.data.new_nick}</ListItem>
                                                </List>       
                                            }
                                        >
                                        </ListItemText>
                                    </ListItem>
                                </List>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        );
    }


    return (
        <ThemeProvider theme={theme}>
            <CssBaseline/>

            {/* Top footer begin */}

            <AppBar position="relative">
                <Toolbar>
                    <TravelExploreIcon sx={{mr: 2}}/>
                    <Typography variant="h6" color="inherit" noWrap>
                        Clouds Website
                    </Typography>
                </Toolbar>
            </AppBar>

            {/* Top footer end */}

            <main>
                <Container sx={{py: 8}} maxWidth="md">
                    <Form></Form>
                </Container>

                {/* Cards begin */}
                <Container sx={{py: 8}} maxWidth="md">
                        
                    <Typography variant="h2" gutterBottom component="div">
                        All Data:
                    </Typography>
                        
                    <RecordsGrid></RecordsGrid>

                    <Typography variant="h5" gutterBottom component="div">
                        Sum of ages: {sumOfAges}
                    </Typography>

                </Container>
            </main>


            {/* Footer begin */}
            <Box sx={{bgcolor: 'background.paper', p: 6}} component="footer">
                <Copyright/>
            </Box>
            {/* End footer */}
        </ThemeProvider>
    );
}