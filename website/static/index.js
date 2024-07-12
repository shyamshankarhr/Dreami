function deleteDream(dreamId){
    fetch('/delete-dream',{
        method: 'POST',
        body: JSON.stringify({ dreamId: dreamId})
    }).then((_res) => {
        window.location.href = "/";
    });
}

