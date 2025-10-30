const API = 'http://localhost:5002';

function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch(`${API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.token) {
      sessionStorage.setItem('token', data.token);  // Lưu vào SessionStorage
      document.getElementById('result').textContent = 'Logged in! Token stored in SessionStorage.';
    } else {
      document.getElementById('result').textContent = data.message;
    }
  });
}

function callProtected() {
  const token = sessionStorage.getItem('token');
  if (!token) {
    document.getElementById('result').textContent = 'No token! Login first.';
    return;
  }

  fetch(`${API}/protected`, {
    headers: { 'Authorization': 'Bearer ' + token }
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('result').textContent = JSON.stringify(data);
  })
  .catch(err => {
    document.getElementById('result').textContent = 'Error: ' + err;
  });
}

function logout() {
  sessionStorage.removeItem('token');
  document.getElementById('result').textContent = 'Logged out. Token removed.';
}