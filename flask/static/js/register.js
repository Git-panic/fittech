// signup.js 파일의 내용

document.addEventListener('DOMContentLoaded', (event) => {
    // 회원가입 폼에 이벤트 리스너를 설정합니다.
    const signupForm = document.querySelector('form');
  
    signupForm.addEventListener('submit', function (event) {
      event.preventDefault(); // 폼의 기본 제출 동작을 중지합니다.
  
      // 폼 데이터를 취합합니다.
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
  
      // 여기서 백엔드 엔드포인트 주소는 실제 서버 설정에 맞춰 변경해야 합니다.
      const signupEndpoint = 'http://127.0.0.1:5000/api/register'; // 이 부분을 실제 회원가입 엔드포인트로 변경하세요.
  
      // fetch API를 사용하여 백엔드로 회원가입 요청을 보냅니다.
      fetch(signupEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          email: email,
          password: password
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Signup failed');
        }
        return response.json();
      })
      .then(data => {
        // 회원가입 성공 후 처리. 예를 들어, 로그인 페이지로 리다이렉트 할 수 있습니다.
        window.location.href = '/login.html'; // 성공 시 이동할 페이지 경로로 변경하세요.
      })
      .catch(error => {
        // 회원가입 실패 시 오류 메시지를 사용자에게 보여줄 수 있습니다.
        console.error('There was an error!', error);
      });
    });
  });
  