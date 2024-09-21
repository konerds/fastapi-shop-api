function submitSigninForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    fetch('/api/members/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.status === 201) {
                alert("로그인에 성공하였습니다!");
                location.href = '/';
                return;
            }
            return response.json().then(dataRaw => {
                throw new Error(dataRaw.detail || '로그인에 실패하였습니다...');
            })
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}