var online='0'
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
async function addCompetition(name,groupNumber,interval,numberOfParticipant,firstNumber, distance, date) {
    const data={'cmd':'addCompetition','competitionName':name, 'groupNumber':groupNumber,'interval':interval,
    'numberOfParticipant':numberOfParticipant,'firstNumber':firstNumber, 'date':date, 'distance':distance};
    const answer=await sendCommandToApi(data);
    return answer;
}
async function updateCompetitionList() {
    const data={'cmd':'getCompetitionList'};
    const answer=await sendCommandToApi(data);
    console.log(answer);
    const  competitionList=document.getElementById('competitionList');
    competitionList.innerHTML='';
    for (i=0;i<answer.length;++i){
        const competitionLine=document.createElement("div");
        competitionLine.setAttribute('id', 'competition_'+answer[i].id);
        competitionList.appendChild(competitionLine);
        const competitionName=document.createElement("span");
        const competitionDate=document.createElement("span");
        competitionLine.appendChild(competitionDate);
        competitionLine.appendChild(competitionName);
        console.log(online)
        if (online==='1'){
        competitionName.innerHTML='<a href="/competition?online=1&competitionID='+answer[i].id+'">'+answer[i].competitionName+'</a>';
        }else{
        competitionName.innerHTML='<a href="/competition?competitionID='+answer[i].id+'">'+answer[i].competitionName+'</a>';

        }
        competitionDate.innerHTML=answer[i].date;
        }


}
document.addEventListener("DOMContentLoaded", async function () {
    console.log('test pay page');
    const queryString = window.location.search;
    console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.get('online')){online=rlParams.get('online')}
    else {online='0'}
    await updateCompetitionList();
    if (online==="1"){
    const competitionForm = document.getElementById('competitionForm');
    if (competitionForm){
        competitionForm.innerHTML="";
        }
        }

});
if (online==='0'){
const sendButton = document.getElementById("sendButton");
    sendButton.addEventListener("click", async (event) => {
      //  clearLanes();
      const competitionName = document.getElementById('competitionName');
      const groupNumber=document.getElementById('groupNumber');
      const interval=document.getElementById('interval');
      const numberOfParticipant=document.getElementById('participantNumber');
      const firstNumber=document.getElementById('startNumber');
      const date=document.getElementById('date')
      const distance=document.getElementById('distance')
      console.log(competitionName.value);
      console.log(groupNumber.value);

      const check1=await addCompetition(competitionName.value,
      groupNumber.value,
      interval.value,
      numberOfParticipant.value,
      firstNumber.value,
      distance.value,
      date.value);
      console.log(check1);
      updateCompetitionList();
    });
}else{
    const competitionForm = document.getElementById('competitionForm');
    if (competitionForm){
        competitionForm.innerHTML="";
        }
}