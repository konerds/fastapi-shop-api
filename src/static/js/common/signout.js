function signout() {
    fetch('/api/members/signout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(_ => {
            location.href = '/';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}