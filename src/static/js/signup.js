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
        .then(response => {
            if (response.status !== 201) {
                throw new Error("회원가입에 실패하였습니다...");
            }
            alert("회원가입에 성공하였습니다!");
            location.href = '/';
        })
        .catch(error => {
            alert(error.message);
            console.error('Error:', error);
        });
}