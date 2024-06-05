document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // 폼 제출 방지

        const formData = {
            'gender': getRadioValue('gender'),
            'age': document.querySelector('input[name="age"]').value,
            'height': document.querySelector('input[name="height"]').value,
            'weight': document.querySelector('input[name="weight"]').value,
            'period': getRadioValue('period'),
            'body': getCheckboxValues('body'),
            'experience': getCheckboxValues('experience'),
            'week': getRadioValue('week'),
            'purpose': getCheckboxValues('purpose')
        };

        // fetch API를 사용하여 백엔드로 데이터 전송
        fetch('/survey_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json(); // 응답을 JSON으로 파싱
            } else {
                throw new Error('Response is not JSON');
            }
        })
        .then(data => {
            console.log(data); // 성공적으로 요청을 처리한 경우
            if (data.message) {
                alert(data.message); // 서버로부터 받은 메시지를 알림으로 표시
                window.location.href = '/recommend';
            } else if (data.error) {
                alert(data.error); // 서버로부터 받은 에러 메시지를 알림으로 표시
            }
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error); // 요청이 실패한 경우
            alert('There was a problem with your fetch operation: ' + error.message); // 사용자에게 에러 메시지 표시
        });
    });

    // 선택된 라디오 버튼 값 가져오는 함수
    function getRadioValue(name) {
        const radios = document.getElementsByName(name);
        for (let i = 0; i < radios.length; i++) {
            if (radios[i].checked) {
                return radios[i].value;
            }
        }
        return null; // 선택된 라디오 버튼이 없는 경우
    }

    // 선택된 체크박스 값 가져오는 함수
    function getCheckboxValues(name) {
        const checkboxes = document.getElementsByName(name);
        const values = [];
        for (let i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                values.push(checkboxes[i].value);
            }
        }
        return values; // 선택된 체크박스 값 배열
    }
});
