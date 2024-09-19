function submitSignupForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        email: formData.get('email'),
        password: formData.get('password'),
        name: formData.get('name')
    };
    fetch('/api/members', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json().then(body => ({status: response.status, body: body})))
        .then(result => {
            if (result.status === 201) {
                alert(result.body.message);
                location.href = '/signin';
            } else {
                throw new Error(result.body.detail || '회원가입에 실패하였습니다...');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert(error.message);
        });
}