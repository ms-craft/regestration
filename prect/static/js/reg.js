const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
$("#signIn").click(function(e) {
	// container.classList.remove("right-panel-active");
    $(".container").removeClass("right-panel-active");
});
$("#signUp").click(function(e) {
	// container.classList.add("right-panel-active");
    $(".container").addClass("right-panel-active");
});

// fistForm.addEventListener("submit", (e) => e.preventDefault());
// secondForm.addEventListener("submit", (e) => e.preventDefault());
// $(function() {
//     $(".button").click(function() {
//         $(".button").addClass("onclic");
//         setTimeout(validate, 250);  // Ждем завершения анимации перед валидацией
//     });

//     function validate() {
//         setTimeout(function() {
//             $(".button").removeClass("onclic");
//             $(".button").addClass("validate");
//             setTimeout(callback, 1250); // Колбэк для удаления класса "validate" через 1250мс
//         }, 2250);  // Ждем завершения анимации перед добавлением класса "validate"
//     }

//     function callback() {
//         $(".button").removeClass("validate");
//     }
// });

// к питону нейросеть
// $(function () {
//     $("#form2").on("submit", function (e) {
//         e.preventDefault(); // Предотвращаем стандартное поведение формы

//         // Получаем данные формы
//         const formData = $(this).serialize();

//         // Отправляем данные на сервер
//         $.post("/register", formData, function (response) {
//             if (response.status === "success") {
//                 $(".button").addClass("onclic");
//                 setTimeout(function () {
//                     $(".button").removeClass("onclic");
//                     $(".button").addClass("validate");

//                     // Изменяем content и background в зависимости от результата
//                     $(".validate").css({
//                         "background": "#1ecd97",
//                         "content": "\f00c" // Используем Unicode для галочки
//                     });

//                     setTimeout(function () {
//                         $(".button").removeClass("validate");
//                     }, 1250);
//                 }, 250);
//             } else {
//                 // Если ошибка, показываем сообщение
//                 $("#result").text(response.message).css("color", "red");
//             }
//         });
//     });
// });