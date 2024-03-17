console.clear();

const cardsContainer = document.querySelector(".cards");
const cardsContainerInner = document.querySelector(".cards__inner");
const cards = Array.from(document.querySelectorAll(".card"));
const overlay = document.querySelector(".overlay");

const applyOverlayMask = (e) => {
  const overlayEl = e.currentTarget;
  const x = e.pageX - cardsContainer.offsetLeft;
  const y = e.pageY - cardsContainer.offsetTop;

  overlayEl.style = `--opacity: 1; --x: ${x}px; --y:${y}px;`;
};

const createOverlayCta = (overlayCard, ctaEl) => {
  const overlayCta = document.createElement("div");
  overlayCta.classList.add("cta");
  overlayCta.textContent = ctaEl.textContent;
  overlayCta.setAttribute("aria-hidden", true);
  overlayCard.append(overlayCta);
};

const observer = new ResizeObserver((entries) => {
  entries.forEach((entry) => {
    const cardIndex = cards.indexOf(entry.target);
    let width = entry.borderBoxSize[0].inlineSize;
    let height = entry.borderBoxSize[0].blockSize;

    if (cardIndex >= 0) {
      overlay.children[cardIndex].style.width = `${width}px`;
      overlay.children[cardIndex].style.height = `${height}px`;
    }
  });
});

const initOverlayCard = (cardEl) => {
  const overlayCard = document.createElement("div");
  overlayCard.classList.add("card");
  createOverlayCta(overlayCard, cardEl.lastElementChild);
  overlay.append(overlayCard);
  observer.observe(cardEl);
};

cards.forEach(initOverlayCard);
document.body.addEventListener("pointermove", applyOverlayMask);


function startCamera() {
  navigator.mediaDevices.getUserMedia({ 
    video: { width: 640, height: 480 } // 카메라 해상도 설정
  })
  .then(stream => {
    let video = document.getElementById('cameraStream');
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("카메라 접근 에러: ", err);
  });
}

// 카메라 스트림을 종료하는 함수
function stopCamera() {
  let video = document.getElementById('cameraStream');
  if (video.srcObject) {
    video.srcObject.getTracks().forEach(track => track.stop());
  }
}

// 모달창 열기 및 카메라 시작
const modal = document.querySelector('dialog');
const btnOpenModal = document.querySelector('.btn-open');
btnOpenModal.addEventListener('click', () => {
  modal.showModal();
  startCamera(); // 카메라 시작
});

// 모달창 닫기 및 카메라 정지
const btnCloseModal = document.querySelector('.btn-close');
btnCloseModal.addEventListener('click', () => {
  modal.close();
  stopCamera(); // 카메라 정지
});
