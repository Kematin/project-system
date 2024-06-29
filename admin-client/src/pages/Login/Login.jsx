import React, { useState } from "react";
import ModalProject from "../../components/ModalProject/ModalProject";
import { useNavigate } from "react-router-dom";
import { loginByUser } from "../../utils/jwtToken";
import "./index.css";

function InputField({ label, value, onChange }) {
  return (
    <div>
      <label className="label-text">{label}</label>
      <input
        className="input-field w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
        value={value}
        onChange={onChange}
        type="text"
      />
    </div>
  );
}

function LoginContent({ setMessage }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function loginInSite(event) {
    event.preventDefault();
    const result = await loginByUser(username, password);
    if (!result) {
      setMessage("Неправильные данные для входа");
    } else {
      navigate("/");
    }
  }
  return (
    <div className="login-content">
      <form onSubmit={loginInSite} className="grid">
        <InputField
          label="Админ"
          value={username}
          onChange={(event) => {
            setUsername(event.target.value);
          }}
        />
        <InputField
          label="Пароль"
          value={password}
          onChange={(event) => {
            setPassword(event.target.value);
          }}
        />
        <button
          className="py-2 px-8 mt-4 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue active:bg-blue-600 transition duration-150 ease-in-out"
          type="submit"
        >
          Войти
        </button>
      </form>
    </div>
  );
}

function Login() {
  const [message, setMessage] = useState("By Kematin");
  return (
    <div id="login-page">
      <ModalProject
        isVisible={true}
        title={<p className="title-login">Войти в админ панель</p>}
        content={<LoginContent setMessage={setMessage} />}
        footer={message}
      />
    </div>
  );
}

export default Login;
