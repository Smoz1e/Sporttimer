var id=0
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


async function updateKPList() {
    const data={'cmd':'getKPList', 'competitionID':id};
    const answer=await sendCommandToApi(data);
    console.log(answer);
    const  kpList=document.getElementById('kpList');
    kpList.innerHTML='';
    for (i=0;i<answer.length;++i){
        const kpLine=document.createElement("div");
        kpLine.setAttribute('id', 'competition_'+answer[i].id);
        kpList.appendChild(kpLine);
        const kpName=document.createElement("span");
        const kpDistance=document.createElement("span");
        kpLine.appendChild(kpDistance);
        kpLine.appendChild(kpName);
        kpName.innerHTML='<a href="/kp?kpID='+answer[i].kpID+'">'+answer[i].kpName+'</a>';
        //kpName.innerHTML='<button id= href="/kp?kpID='+answer[i].kpID+'">'+answer[i].kpName+'</button><div id="kp1_rez"+answer.id';
        kpDistance.innerHTML=answer[i].kpDistance;
        }


}

async function printParticipantList() {
    const data={'cmd':'getParticipantList', 'competitionID':id};
    const answer=await sendCommandToApi(data);
    const participantList=document.getElementById('participantList');
    participantList.innerHTML='';
    for (i=0;i<answer.length;++i){
        const participantLine=document.createElement("div");
        participantLine.setAttribute('id', 'competition_'+answer[i].id);
        participantList.appendChild(participantLine);
        const participantName=document.createElement("span");
        const participantNumber=document.createElement("span");
        const startTime=document.createElement("span");
        participantLine.appendChild(participantNumber);
        participantLine.appendChild(participantName);
        participantLine.appendChild(startTime);
        participantNumber.innerHTML=answer[i].startNumber;
        participantName.innerHTML=answer[i].participantName;
        startTime.innerHTML=answer[i].startTime;
        }
}

document.addEventListener("DOMContentLoaded", async function () {
    const queryString = window.location.search;
    console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    id = urlParams.get('competitionID');
    console.log(id);
    await updateKPList();

    await printParticipantList();
});

async function addKP(kpName, kpDistance) {
    const data={'cmd':'addKP','kpName':kpName,'kpDistance':kpDistance, 'competitionID':id};
    const answer=await sendCommandToApi(data);
    return answer;
}

async function addTime(startTime) {
    const data={'cmd':'addTime','startTime':startTime, 'competitionID':id};
    console.log(startTime);
    const answer=await sendCommandToApi(data);
    return answer;
}


const addKPButton = document.getElementById("addKPButton");
    addKPButton.addEventListener("click", async (event) => {
      //  clearLanes();
      const kpName = document.getElementById('kpName');
      const kpDistance=document.getElementById('kpDistance');

      const check1=await addKP(kpName.value,
      kpDistance.value);
      console.log(check1);
      updateKPList();
    });

const startButton = document.getElementById("startButton");
    startButton.addEventListener("click", async (event) => {
      //  clearLanes();
      const startTime= new Date();
      //console.log(startTime);
      const check1=await addTime(startTime);


    });


    setInterval(function () {
 date = new Date();


  h = date.getHours();
   m = date.getMinutes();
   s = date.getSeconds();


 h = (h < 10) ? '0' + h : h;
 m = (m < 10) ? '0' + m : m;
 s = (s < 10) ? '0' + s : s;

 document.getElementById('time').innerHTML =  h + ':' + m + ':' + s;
}, 1000);