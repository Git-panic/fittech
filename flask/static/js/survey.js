document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const data = {};
        
        formData.forEach((value, key) => {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/survey_answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();

            if (result.success) {
                alert(result.message);
                window.location.href = '/recommend';
            } else {
                alert('설문을 제출하는 중 문제가 발생했습니다: ' + result.message);
            }
        } catch (error) {
            alert('설문을 제출하는 중 문제가 발생했습니다: ' + error.message);
        }
    });
});

