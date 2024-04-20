// survey.js 파일의 내용

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');

  form.addEventListener('submit', function(event) {
      event.preventDefault(); // 폼 제출 방지

      const formData = {
          'gender': getRadioValue('gender'),
          'age': getRadioValue('age'),
          'difficulty': getRadioValue('difficulty'),
          'purpose': getRadioValue('purpose'),
          'body': getRadioValue('body'),
          'time': getRadioValue('time')
      };

      // fetch API를 사용하여 백엔드로 데이터 전송
      fetch('/survey', {
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
          return response.json();
      })
      .then(data => {
          console.log(data); // 성공적으로 요청을 처리한 경우
      })
      .catch(error => {
          console.error('There was a problem with your fetch operation:', error); // 요청이 실패한 경우
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
});