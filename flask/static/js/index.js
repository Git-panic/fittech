// 백엔드 API로 GET 요청을 하는 예제 함수
async function fetchData(url) {
    try {
        let response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP 오류! 상태: ${response.status}`);
        }
        let data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch 오류:', error);
    }
}

// 사용 예시: fetchData('https://your-backend-api.com/data')
