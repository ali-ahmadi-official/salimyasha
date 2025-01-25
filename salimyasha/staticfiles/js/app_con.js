const daysOfWeek = ['شنبه', 'یک‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'];
let today = new Date().getDay();
today = (today + 8) % 7;
document.getElementById('today').innerText = `امروز`;
document.getElementById('ctoday').innerText = `امروز`;
document.getElementById('tomorrow').innerText = `فردا`;
document.getElementById('ctomorrow').innerText = `فردا`;
for (let i = 2; i <= 6; i++) {
    document.getElementById(`day-${i}`).innerText = `${daysOfWeek[(today + i) % 7]}`;
    document.getElementById(`cday-${i}`).innerText = `${daysOfWeek[(today + i) % 7]}`;
}

const btnToday = document.getElementById('today').addEventListener('click', () => {
    let title = document.querySelector('.time-title');
    title.innerHTML = 'نوبت های آزاد امروز';
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.today-time');
    day.style.display = 'flex';
});

const cbtnToday = document.getElementById('ctoday').addEventListener('click', () => {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = 'مشاوره های آزاد امروز';
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.ctoday-time');
    day.style.display = 'flex';
});

const btnTomorrow = document.getElementById('tomorrow').addEventListener('click', function tomorrow() {
    let title = document.querySelector('.time-title');
    title.innerHTML = 'نوبت های آزاد فردا';
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.tomorrow-time');
    day.style.display = 'flex';
});

const cbtnTomorrow = document.getElementById('ctomorrow').addEventListener('click', function tomorrow() {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = 'مشاوره های آزاد فردا';
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.ctomorrow-time');
    day.style.display = 'flex';
});

const btn2 = document.getElementById('day-2').addEventListener('click', function day2() {
    let title = document.querySelector('.time-title');
    title.innerHTML = `نوبت های آزاد ${daysOfWeek[(today + 2) % 7]}`;
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.day-2-time');
    day.style.display = 'flex';
});

const cbtn2 = document.getElementById('cday-2').addEventListener('click', function day2() {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = `مشاوره های آزاد ${daysOfWeek[(today + 2) % 7]}`;
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.cday-2-time');
    day.style.display = 'flex';
});

const btn3 = document.getElementById('day-3').addEventListener('click', function day3() {
    let title = document.querySelector('.time-title');
    title.innerHTML = `نوبت های آزاد ${daysOfWeek[(today + 3) % 7]}`;
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.day-3-time');
    day.style.display = 'flex';
});

const cbtn3 = document.getElementById('cday-3').addEventListener('click', function day3() {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = `مشاوره های آزاد ${daysOfWeek[(today + 3) % 7]}`;
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.cday-3-time');
    day.style.display = 'flex';
});

const btn4 = document.getElementById('day-4').addEventListener('click', function day4() {
    let title = document.querySelector('.time-title');
    title.innerHTML = `نوبت های آزاد ${daysOfWeek[(today + 4) % 7]}`;
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.day-4-time');
    day.style.display = 'flex';
});

const cbtn4 = document.getElementById('cday-4').addEventListener('click', function day4() {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = `مشاوره های آزاد ${daysOfWeek[(today + 4) % 7]}`;
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.cday-4-time');
    day.style.display = 'flex';
});

const btn5 = document.getElementById('day-5').addEventListener('click', function day5() {
    let title = document.querySelector('.time-title');
    title.innerHTML = `نوبت های آزاد ${daysOfWeek[(today + 5) % 7]}`;
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.day-5-time');
    day.style.display = 'flex';
});

const cbtn5 = document.getElementById('cday-5').addEventListener('click', function day5() {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = `مشاوره های آزاد ${daysOfWeek[(today + 5) % 7]}`;
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.cday-5-time');
    day.style.display = 'flex';
});

const btn6 = document.getElementById('day-6').addEventListener('click', function day6() {
    let title = document.querySelector('.time-title');
    title.innerHTML = `نوبت های آزاد ${daysOfWeek[(today + 6) % 7]}`;
    const times = document.querySelectorAll('.time');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.day-6-time');
    day.style.display = 'flex';
});

const cbtn6 = document.getElementById('cday-6').addEventListener('click', function day6() {
    let title = document.querySelector('.ctime-title');
    title.innerHTML = `مشاوره های آزاد ${daysOfWeek[(today + 6) % 7]}`;
    const times = document.querySelectorAll('.ctime');
    times.forEach(time => {
        time.style.display = 'none';
    });
    const day = document.querySelector('.cday-6-time');
    day.style.display = 'flex';
});