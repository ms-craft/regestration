// Получение всех пользователей
// async function getUsers() {
//     // отправляет запрос и получаем ответ
//     const response = await fetch("/api/users", {
//         method: "GET",
//         headers: { "Accept": "application/json" }
//     });
//     // если запрос прошел нормально
//     if (response.ok === true) {
//         // получаем данные
//         const users = await response.json();
//         const rows = document.querySelector("tbody");
//         // добавляем полученные элементы в таблицу
//         users.forEach(user => rows.append(row(user)));
//     }
// }
// Получение одного пользователя
async function getUser(id) {
    const response = await fetch(`/api/users/${id}`, {
        method: "GET",
        headers: { "Accept": "application/json" }
    });
    if (response.ok === true) {
        const user = await response.json();
        document.getElementById("userId").value = user.id;
        document.querySelector(".userPassword").value = user.name;
        document.querySelector(".userEmail").value = user.email;
        document.querySelector(".userLogin").value = user.login;
        
    }
    else {
        // если произошла ошибка, получаем сообщение об ошибке
        const error = await response.json();
        console.log(error.message); // и выводим его на консоль
    }
}
// Добавление пользователя
async function createUser(userPassword, passPasword, userEmail, userLogin) {
    
        const response = await fetch("api/users", {
            method: "POST",
            headers: { "Accept": "application/json", "Content-Type": "application/json" },
            body: JSON.stringify({
                password: userPassword,
                login: userLogin,
                email: userEmail

            })
        });
        if (response.ok === true) {
            const user = await response.json();
            // document.querySelector("tbody").append(row(user));
            console.log(user)

            setTimeout(function () {
                $(".button").removeClass("onclic");
                $(".button").addClass("validate success");

                // Изменяем content и background в зависимости от результата
                
                $(".validate").css({
                    "background": "#1ecd97",
                });

                setTimeout(function () {
                    $(".button").removeClass("validate").css("background", "");
                    $("button").removeClass("success")
                }, 950);
                setTimeout(function () {
                    $(".container").removeClass("right-panel-active");
                }, 1000)
            }, 550);
        }
        else {
            const error = await response.json();
            console.log(error.message);
            setTimeout(function () {
                $(".button").removeClass("onclic");
                $(".button").addClass("validate");
                setTimeout(function () {
                    $(".button").removeClass("validate").css("background", "");
                }, 1550);
            }, 550);
        }
    }
    
// Изменение пользователя
// async function editUser(userId, userPassword, userLogin) {
//     const response = await fetch("api/users", {
//         method: "PUT",
//         headers: { "Accept": "application/json", "Content-Type": "application/json" },
//         body: JSON.stringify({
//             id: userId,
//             name: userPassword,
//             login: userLogin
//         })
//     });
//     if (response.ok === true) {
//         const user = await response.json();
//         document.querySelector(`tr[data-rowid='${user.id}']`).replaceWith(row(user));
//     }
//     else {
//         const error = await response.json();
//         console.log(error.message);
//     }
// }
// Удаление пользователя
async function deleteUser(id) {
    const response = await fetch(`/api/users/${id}`, {
        method: "DELETE",
        headers: { "Accept": "application/json" }
    });
    if (response.ok === true) {
        const user = await response.json();
        document.querySelector(`tr[data-rowid='${user.id}']`).remove();
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }
}

// сброс данных формы после отправки
// function reset() {
//     document.getElementById("userId").value = 
//     document.getElementById("userPassword").value = 
//     document.getElementById("userLogin").value = "";
// }
// создание строки для таблицы
// function row(user) {

//     const tr = document.createElement("tr");
//     tr.setAttribute("data-rowid", user.id);

//     const nameTd = document.createElement("td");
//     nameTd.append(user.name);
//     tr.append(nameTd);

//     const ageTd = document.createElement("td");
//     ageTd.append(user.login);
//     tr.append(ageTd);

//     const linksTd = document.createElement("td");

//     const editLink = document.createElement("button"); 
//     editLink.append("Изменить");
//     editLink.addEventListener("click", async() => await getUser(user.id));
//     linksTd.append(editLink);

//     const removeLink = document.createElement("button"); 
//     removeLink.append("Удалить");
//     removeLink.addEventListener("click", async () => await deleteUser(user.id));

//     linksTd.append(removeLink);
//     tr.appendChild(linksTd);

//     return tr;
// }
// сброс значений формы
// document.getElementById("resetBtn").addEventListener("click", () =>  reset());

function sanitizeInput(input) {
    const sqlInjectionPattern = /['"\\;]/g; // Признаки SQL инъекций
    return input.replace(sqlInjectionPattern, '');
}

// Проверка логина
function validateLogin() {
    const userLogin = document.querySelector('.userLogin').value;
    const sanitizedLogin = sanitizeInput(userLogin); // Санитизация логина
    document.querySelector('.userLogin').value = sanitizedLogin; // Обновление значения

    const loginPattern = /^[a-zA-Z0-9]{3,}$/;
    if (!loginPattern.test(sanitizedLogin)) {
        console.log('Логин должен содержать минимум 3 символа и только английские буквы');
        return false;
    } else {
        // loginError.textContent = '';
        return true;
    }
}

function validatePassword() {
    const userPassword = document.querySelector('.userPassword').value;
    const passPassword = document.querySelector('.passPassword').value;

    if (userPassword.length < 8) {
        console.log('Пароль должен содержать минимум 8 символов');
        return false;
    } else {
        return true;
    }
}

function validateEmail() {
    const userEmail = document.querySelector('.userEmail').value;
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!emailPattern.test(userEmail)) {
        console.log('Неверный формат email');
        return false;
    } else {
        return true;
    }
}
function validatePassPassword() {
    const userPassword = document.querySelector('.userPassword').value;
    const passPassword = document.querySelector('.passPassword').value;

    if (userPassword !== passPassword) {
        console.log('Пароли не совпадают');
        return false;
    } else {
        return true;
    }
}


// отправка формы
// const fields = [
//     { id: '.userLogin', validate: validateLogin },
//     { id: '.userPassword', validate: validatePassword },
//     { id: '.passPassword', validate: validatePassPassword },
//     { id: '.userEmail', validate: validateEmail }
// ];

// fields.forEach(field => {
//     document.querySelector(field.id).addEventListener('blur', field.validate);
// });

// fistForm.addEventListener("submit", (e) => e.preventDefault());
// $(".form").click((e) => e.preventDefault());

document.querySelector(".signUp").addEventListener("click", async (e) => {
    e.preventDefault();
    $(".button").addClass("onclic"); 
    const isLoginValid = validateLogin();
    const isPasswordValid = validatePassword();
    const isPassPasswordValid = validatePassPassword();
    const isEmailValid = validateEmail();
    // Если все поля валидны, продолжаем отправку данных
    if (isLoginValid && isPasswordValid && isPassPasswordValid && isEmailValid) {
        const id = document.getElementById("userId").value;
        const password = document.querySelector(".userPassword").value;
        const passPasword = document.querySelector(".passPassword").value;
        const email = document.querySelector(".userEmail").value;
        const login = document.querySelector(".userLogin").value;
        if (id === "")
            await createUser(password, passPasword, email, login);
        // else
        //     await editUser(id, name, email, login);
        // reset();
    } else {
        console.log('не правильно тут все');
       
        setTimeout(function () {
            $(".button").removeClass("onclic");
            $(".button").addClass("validate");
            setTimeout(function () {
                $(".button").removeClass("validate").css("background", "");
            }, 1550);
        }, 550);
        setTimeout(function () {
            if (!isLoginValid) {
                document.querySelector(".userLogin").classList.add("input-error");
            }
            if (!isPasswordValid) {
                document.querySelector(".userPassword").classList.add("input-error");
            }
            if (!isPassPasswordValid) {
                document.querySelector(".passPassword").classList.add("input-error");
            }
            if (!isEmailValid) {
                document.querySelector(".userEmail").classList.add("input-error");
            }
        }, 900)
    }
});

document.querySelector(".LogIn").addEventListener("click", async (e) => {
    e.preventDefault();
    $(".button").addClass("onclic"); 
    const id = document.getElementById("userIdLogin").value;
    const email = document.querySelector(".name").value;
})
// загрузка пользователей
// getUsers();
