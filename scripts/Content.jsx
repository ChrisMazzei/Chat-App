    
import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('messages received', updateMessages);
            return () => {
                Socket.off('messages received', updateMessages);
            }
        });
    }
    
    function updateMessages(data) {
        console.log("Received message from server: " + data['allMessages']);
        setMessages(data['allMessages']);
    }
    
    getNewAddresses();
    
    const navstyle = {
        top: "0",
        height: "700px",
        width: "100%",
        overflow:"hidden",
        'overflow-y':"scroll",
        'background-image': "url(https://img.freepik.com/free-photo/empty-wooden-table-with-smoke-float-up-dark-background_68495-135.jpg?size=626&ext=jpg)"
    };
    
    const divstyle = {
        width: "50%",
	    height: "100px",
    	position: "absolute",
    	top:"0",
    	left: "0",
    	right: "0",
    	margin: "auto"
    };
    
    const liststyle = {
        'text-align': "left",
        'list-style-type': "none"
    };
    
    const textstyle = {
        color: "#F0F8FF"
    };
    
    const bodyimage = {
      'background-image': "url(https://image.freepik.com/free-vector/abstract-3d-vector-technology-dark-gray-background_87538-28.jpg)"  
    };
    const backgroundImg = "https://img.freepik.com/free-photo/empty-wooden-table-with-smoke-float-up-dark-background_68495-135.jpg?size=626&ext=jpg";
    return (
        <html>
        <head>
        </head>
        <body>
        
        <div style={divstyle}>
            <h1>Welcome to the Chat Room!</h1>
                <nav id="chat" style={navstyle}>
                    <ol style={liststyle}>
                        {
                            messages.map((message, index) =>
                            <li style={textstyle} key={index}>{message}</li>)
                        }
                    </ol>
                </nav>
            <Button />
        </div>
        </body>
        </html>
    );
}
