let last_event_id=0;

async function get_events(id) {
    const url = "./sb_call_api";
    const data = { cmd: 'getevents',id:id };

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    };

    try {
        const response = await fetch(url, options);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(response.statusText);
        }
    } catch (e) {
        throw new Error(e);
    }
}
async function update_events()
{
    let Data = await get_events(last_event_id);
    let events  = Data.events;

    for (let i=0;i<events.length;i++){
        //console.log(events[i].event);

        if (events[i].event==='guest_call'){

            //console.log('button'+events[i].button_id+' = guest call');
            var table_button=document.getElementById('Button'+events[i].button_id);
            if (table_button){
                table_button.classList="glare-button";
                soundClick;
            }
        } else if (events[i].event==='staff_call'){
            var table_button=document.getElementById('Button'+events[i].button_id);
            if (table_button){
                table_button.classList="glare-button-l";
        }
        if (last_event_id<events[i].id){
            last_event_id=events[i].id;
        }
    }

    }
}
async function send_events(button_id,event){
    const url = "./sb_call_api";
    const data = { cmd: 'sendevents',button_id:button_id,event:event };

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    };

    try {
        const response = await fetch(url, options);
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(response.statusText);
        }
    } catch (e) {
        throw new Error(e);
    }
}
function soundClick() {
  var audio = new Audio(); // Создаём новый элемент Audio
  audio.src = '/static/bell.mp3'; // Указываем путь к звуку "клика"
  audio.autoplay = true; // Автоматически запускаем
}
function set_buttonstyle_staff_call(button_id)
{
    var table_button=document.getElementById('Button'+button_id);
            if (table_button){
                table_button.classList="glare-button-l";
            }

}
document.addEventListener("DOMContentLoaded", async function () {

    let currentChatCount = 0;
    //const chatMessages = document.getElementById('TableEvents');
    //chatMessages.innerHTML = "";

    const Data = await get_events(0);

    console.log(Data);
    let events = Data.events;


    for (let i=0;i<events.length;i++){
        console.log(events[i].event);

        if (events[i].event==='guest_call'){

            console.log('button'+events[i].button_id+' = guest call');
            var table_button=document.getElementById('Button'+events[i].button_id);
            if (table_button){
                //table_button.classList.add("glare-button");
                table_button.classList="glare-button";

            }
        }
        if (last_event_id<events[i].id){
            last_event_id=events[i].id;
        }

        jsonData = events[i];
        for (var key in jsonData) {
            if (jsonData.hasOwnProperty(key)) {
                 console.log(key + " -> " + jsonData[key]);
         }
    }

    }

    });
document.getElementById("Button1").addEventListener("click", async () => {
    button_id=1;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button2").addEventListener("click", async () => {
    button_id=2;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button3").addEventListener("click", async () => {
    button_id=3;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button4").addEventListener("click", async () => {
    button_id=4;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button5").addEventListener("click", async () => {
    button_id=5;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button6").addEventListener("click", async () => {
    button_id=6;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button7").addEventListener("click", async () => {
    button_id=7;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button8").addEventListener("click", async () => {
    button_id=8;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button9").addEventListener("click", async () => {
    button_id=9;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button10").addEventListener("click", async () => {
    button_id=10;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button11").addEventListener("click", async () => {
    button_id=11;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button12").addEventListener("click", async () => {
    button_id=12;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button13").addEventListener("click", async () => {
    button_id=13;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button14").addEventListener("click", async () => {
    button_id=14;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button15").addEventListener("click", async () => {
    button_id=15;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button16").addEventListener("click", async () => {
    button_id=16;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});
document.getElementById("Button17").addEventListener("click", async () => {
    button_id=17;
    await send_events(button_id,'staff_call');
    set_buttonstyle_staff_call(button_id);

});


setInterval(update_events, 1000);
    // Сд



   //setInterval(get_events(0), 1000);
