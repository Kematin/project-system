import Cookies from "universal-cookie";

const cookies = new Cookies();

async function loginByCookies() {
  const username = cookies.get("admin_username");
  const password = cookies.get("admin_password");
  if (username && password) {
    const token = await loginByUser(username, password);
    if (token) {
      return token;
    } else {
      window.location.href = "/login";
      return false;
    }
  }
  window.location.href = "/login";
  return false;
}

export async function loginByUser(username, password) {
  try {
    const response = await fetch(`http://kematin.space:9999/admin/auth`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });
    if (response.ok) {
      const responseData = await response.json();
      cookies.set("admin_username", username);
      cookies.set("admin_password", password);
      cookies.set("token", responseData.access_token);
      return responseData.access_token;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}

export async function getToken() {
  let token = cookies.get("token");
  if (token) {
    const response = await fetch(
      `http://kematin.space:9999/admin/check_token?token=${token}`,
      {}
    );

    if (response.ok) {
    } else {
      token = await loginByCookies();
    }
  } else {
    token = await loginByCookies();
  }
  return token;
}
