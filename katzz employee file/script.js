let employees = JSON.parse(localStorage.getItem("employees")) || [];
let selectedName = null;

function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;
  if (user === "admin" && pass === "admin") {
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("mainApp").style.display = "block";
    loadEmployees();
  } else {
    alert("Wrong credentials");
  }
}

function addEmployee() {
  const name = document.getElementById("empName").value;
  const position = document.getElementById("empPosition").value;
  if (!name || !position) return alert("Please fill all fields");

  employees.push({ name, position, attendance: "Absent" });
  saveAndReload();
}

function updateEmployee() {
  const name = document.getElementById("empName").value;
  const position = document.getElementById("empPosition").value;

  const emp = employees.find(e => e.name === selectedName);
  if (emp) {
    emp.name = name;
    emp.position = position;
    saveAndReload();
  } else {
    alert("Employee not selected or not found");
  }
}

function deleteEmployee() {
  employees = employees.filter(e => e.name !== document.getElementById("empName").value);
  saveAndReload();
}

function loadEmployees() {
  const table = document.querySelector("#employeeTable tbody");
  table.innerHTML = "";
  employees.forEach(emp => {
    const row = document.createElement("tr");
    row.innerHTML = <td>${emp.name}</td><td>${emp.position}</td><td>${emp.attendance}</td>;
    row.onclick = () => {
      document.getElementById("empName").value = emp.name;
      document.getElementById("empPosition").value = emp.position;
      selectedName = emp.name;
    };
    table.appendChild(row);
  });
}

function searchEmployee() {
  const term = document.getElementById("search").value.toLowerCase();
  document.querySelectorAll("#employeeTable tbody tr").forEach(row => {
    const name = row.children[0].innerText.toLowerCase();
    row.style.display = name.includes(term) ? "" : "none";
  });
}

function recordAttendance() {
  if (!selectedName) return alert("Select an employee to mark present");
  const emp = employees.find(e => e.name === selectedName);
  if (emp) {
    emp.attendance = "Present";
    saveAndReload();
  }
}

function generateReport() {
    let content = "Name,Position,Attendance\n";
    employees.forEach(e => {
      content += ${e.name},${e.position},${e.attendance}\n;  // <-- Backticks used here
    });
  
    const blob = new Blob([content], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "employee_report.csv";
    a.click();
  }


function saveAndReload() {
  localStorage.setItem("employees", JSON.stringify(employees));
  loadEmployees();
  document.getElementById("empName").value = "";
  document.getElementById("empPosition").value = "";
  selectedName = null;
}