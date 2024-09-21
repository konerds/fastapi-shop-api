function signout() {
    fetch('/api/members/signout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json().then(dataRaw => {
            if (!response.ok) {
                throw new Error(dataRaw.detail || "로그아웃하는 동안 문제가 발생하였습니다...");
            }
            alert("로그아웃되었습니다!")
            location.href = '/';
        }))
        .catch((error) => {
            console.error('Error:', error);
        });
}