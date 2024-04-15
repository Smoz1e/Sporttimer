online='0'
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
        competitionName.innerHTML='<a href="/kp?online=1&kpID='+answer[i].finishKP+'">'+answer[i].competitionName+'</a>';
        competitionDate.innerHTML=answer[i].date;
        }


}
document.addEventListener("DOMContentLoaded", async function () {
    console.log('test pay page');
    const queryString = window.location.search;
    console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.get('online')){online=urlParams.get('online')}
    else {online='0'}
    await updateCompetitionList();


});