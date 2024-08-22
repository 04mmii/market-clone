const form = document.querySelector("#login-form");

const handleSubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });

  const data = await res.json();
  accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인 되었습니다.");

  window.location.pathname = "/";

  const btn = document.createElement("button");
  btn.innerText = "상품 가져오기!";
  btn.addEventListener("click", async () => {
    const res = await fetch("/items", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    const data = await res.json();
  });
  infoDiv.appendChild(btn);

  //   if (res.status === 200) {
  //     alert("로그인에 성공했습니다!");
  //     window.location.pathname = "/";
  //   } else if (res.status === 401) {
  //     alert("id혹은 password가 틀렸습니다.");
  //   }
};

form.addEventListener("submit", handleSubmit);
