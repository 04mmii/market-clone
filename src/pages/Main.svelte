<script>
  let hour = new Date().getHours();
  let min = new Date().getMinutes();
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/chart-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <img src="assets/arrow.svg" alt="arrow" />
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/menu.svg" alt="menu" />
      <img src="assets/alert.svg" alt="alert" />
    </div>
  </div>
</header>

<main>
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>
<!-- //main -->

<footer>
  <div class="footer-block">
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/home.svg" alt="home" />
      </div>
      <div>홈</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/docu.svg" alt="docu" />
      </div>
      <div>동네생활</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/location.svg" alt="location" />
      </div>
      <div>내근처</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/chat.svg" alt="chat" />
      </div>
      <div>채팅</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/user.svg" alt="user" />
      </div>
      <div>나의 당근</div>
    </div>
  </div>
</footer>
<!-- //footer -->
<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>
