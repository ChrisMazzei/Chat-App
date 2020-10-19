import * as React from 'react';
import { Socket } from './Socket';


function updateScroll() {
        var element = document.getElementById("chat");
        element.scrollTop = element.scrollHeight;
        element.animate({scrollTop: element.scrollHeight});
}

function handleSubmit(event) {
    let newMessage = document.getElementById("message_input");
    let nickName = document.getElementById("nick_name");
    
    Socket.emit('new message input', {
        'message': newMessage.value, 'nickname' : nickName.value
    });
    
    console.log('Sent the address ' + newMessage.value + ' to server!');
    newMessage.value = ''
    
    event.preventDefault();
    updateScroll();
}

const messagebox = {
    width: "100%",
    height: "40px"
};

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="message_input" style={messagebox} placeholder="Enter a message!"></input>
            <input id="nick_name" placeholder="Enter a nick name!"></input>
            <button>Send</button>
        </form>
    );
}
