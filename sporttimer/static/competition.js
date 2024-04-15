var id=0 //competition id
var kpID=0
var online="0"
async function sendCommandToApi(data) //отправляет data на сервер
{
    const url = "/sporttimer_api";

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
    } catch (error) {
        throw error;
    }
}


async function getCompetitionID() {
    const data={'cmd':'getCompetitionID', 'kpID':kpID};
    const answer=await sendCommandToApi(data);
    id=answer.competitionID;
}


async function getParticipantPlace() {
    const data = {'cmd':'getParticipantPlace', 'kpID':kpID,'participantNumber':participantNumber};

    const answer = await sendCommandToApi(data);

}


async function stopParticipantF(participantNumber,participantName,startTime) {
    date = new Date();
    h = date.getHours();
    m = date.getMinutes();
    s = date.getSeconds();
    const time=h+':'+m+':'+s;
    const data={'cmd':'stopParticipant', 'kpID':kpID, 'competitionID':id,
    'participantNumber':participantNumber,'participantName':participantName,'startTime':startTime, 'finshTime':date};
    const answer= await sendCommandToApi(data);
    return answer;
}
async function updateKPList() {
    const data={'cmd':'getKPList', 'competitionID':id};
    const answer=await sendCommandToApi(data);
    console.log(answer);
    const  kpList=document.getElementById('kpList');
    kpList.innerHTML='';
    for (i=0;i<answer.length;++i){
        const kpLine=document.createElement("div");
        kpLine.setAttribute('id', 'competition_'+id);
        kpList.appendChild(kpLine);
        const kpName=document.createElement("span");
        const kpDistance=document.createElement("span");
        kpLine.appendChild(kpDistance);
        kpLine.appendChild(kpName);
        if (online==='1'){

            kpName.innerHTML='<a href="/kp?online=1&kpID='+answer[i].kpID+'">'+answer[i].kpName+'</a>';
        }else{
            kpName.innerHTML='<a href="/kp?kpID='+answer[i].kpID+'">'+answer[i].kpName+'</a>';}
        //kpName.innerHTML='<button id= href="/kp?kpID='+answer[i].kpID+'">'+answer[i].kpName+'</button><div id="kp1_rez"+answer.id';
        kpDistance.innerHTML=answer[i].kpDistance;
        }


}
async function printParticipantList(kpID) {
    console.log(id);
    const data={'cmd':'getParticipantList', 'competitionID':id,'kpID':kpID};
    const answer=await sendCommandToApi(data);
    console.log(answer);
    const participantList=document.getElementById('participantList');
    participantList.innerHTML='';
    for (i=0;i<answer.length;++i){
        const participantLine=document.createElement("div");
        //participantLine.style.backgroundColor='#B2DFDB';
        //participantLine.style.display='block';
        //participantLine.style.border='3px solid #132D8D'

        participantLine.className='line';
        participantLine.setAttribute('id', 'competition_'+answer[i].id);
        participantList.appendChild(participantLine);
        const participantNumber=document.createElement("span");
        const participantName=document.createElement("span");

        const participantPlace=document.createElement("div");
        participantPlace.id="place"+answer[i].startNumber;
        participantPlace.innerHTML=answer[i].place;

        const participantDelta=document.createElement("div");
        participantDelta.id='delta'+answer[i].startNumber;
        participantDelta.innerHTML=answer[i].resultDelta;

        const participantResult=document.createElement("div");
        participantResult.id='result'+answer[i].startNumber;
        participantResult.innerHTML=answer[i].resultTime;

        const startTime=document.createElement("span");
        participantName.className='cell-name';
        participantNumber.className='cell-num';
        startTime.className='cell';
        participantResult.className='cell-res';
        participantDelta.className='cell-delta';
        participantPlace.className='cell-place';
        participantLine.appendChild(participantNumber);
        participantLine.appendChild(participantName);
        participantLine.appendChild(participantPlace);
        participantLine.appendChild(participantDelta);
        participantLine.appendChild(participantResult);
        participantLine.appendChild(startTime);
        participantNumber.innerHTML=answer[i].startNumber;
        //participantName.innerHTML=answer[i].participantName;
        if (online==="1"){
            participantName.innerHTML='<div class="cell-but" +id="stopParticipant'+answer[i].startNumber+'">'+answer[i].participantName+
'</div>';
        }else{participantName.innerHTML='<div class="cell-but" ><button class="cell-but" id="stopParticipant'+answer[i].startNumber+'">'+answer[i].participantName+
        '</button></div>';
        }

        //<div id="place'+answer[i].startNumber+'"></div><div id="delta'+answer[i].startNumber+'"></div><div id="result'+answer[i].startNumber+'"></div>';

        const buttonID=answer[i].startNumber;
        const name=answer[i].participantName;
        const sttime=answer[i].startTime;

        //console.log(buttonID)
        if (online==='0'){
            const stopParticipant = document.getElementById('stopParticipant'+buttonID);
            stopParticipant.addEventListener("click", async(event) => {
            console.log(buttonID);
            const result=await stopParticipantF(buttonID,name,sttime);
            console.log(result)
            for (j=0;j<result.length;++j){
                result[j]
                const divIDPlace="place"+result[j].startNumber;
                const divDelta="delta"+result[j].startNumber;
                const divResult="result"+result[j].startNumber;
                const participantPlace=document.getElementById(divIDPlace);
                const participantDelta=document.getElementById(divDelta);
                const participantResult=document.getElementById(divResult);
                participantPlace.innerHTML=result[j].place;
                participantResult.innerHTML=result[j].finshResult;
                participantDelta.innerHTML=result[j].delta;


            }
            //console.log(result);




            });
        }
        startTime.innerHTML=answer[i].startTime;
    }

        }



document.addEventListener("DOMContentLoaded", async function () {
    const queryString = window.location.search;
    console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    kpID = urlParams.get('kpID');
    if (urlParams.get('online')){online=urlParams.get('online')}
    else {online='0'}

    console.log(online);
    if (id===0){await getCompetitionID();}

    await updateKPList();
    //console.log(id);
    await printParticipantList(kpID);

    if (online==="1"){

        setInterval(async function() {
        if(document.hidden === false) {
            await printParticipantList(kpID);
            }
            }, 3000);
    }
    else {
    await printParticipantList(kpID);
    }

});


