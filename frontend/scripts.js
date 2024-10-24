// Скрипт для смены видео на фоне

document.addEventListener('DOMContentLoaded', function () {
    const videos = [
        document.getElementById('video1'),
        document.getElementById('video2'),
        document.getElementById('video3'),
        document.getElementById('video4')
    ];
    let currentVideoIndex = 0;

    function switchVideo() {
        videos[currentVideoIndex].style.display = 'none';
        currentVideoIndex = (currentVideoIndex + 1) % videos.length;
        videos[currentVideoIndex].style.display = 'block';
    }

    setInterval(switchVideo, 2000);

    const fadeElements = document.querySelectorAll('.fade-in');

    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    fadeElements.forEach(element => {
        observer.observe(element);
    });
});

// Скрипт для смены языка

let currentLanguage = "en";

function loadLanguageContent(lang) {
    fetch(`assets/${lang}.json`)
        .then(response => response.json())
        .then(data => {
            document.querySelector(".hero-title").innerHTML = data.heroTitle;
            document.querySelector(".hero-description").innerHTML = data.heroDescription;
            document.querySelector(".comic-1-1").innerHTML = data.comic11;
            document.querySelector(".comic-1-2").innerHTML = data.comic12;
            document.querySelector(".comic-1-3").innerHTML = data.comic13;
            document.querySelector(".video-title").innerHTML = data.videoTitle;
            document.querySelector(".video-description-1").innerHTML = data.videoDescription1;
            document.querySelector(".video-description-2").tinnerHTML= data.videoDescription2;
            document.querySelector(".video-description-3").innerHTML = data.videoDescription3;
            document.querySelector(".video-description-4").innerHTML = data.videoDescription4;
            document.querySelector(".video-description-5").innerHTML = data.videoDescription5;
            document.querySelector(".video-description-6").innerHTML = data.videoDescription6;
            document.querySelector(".video-description-7").innerHTML = data.videoDescription7;
            document.querySelector(".comic-2-1").innerHTML = data.comic21;
            document.querySelector(".comic-2-2").innerHTML = data.comic22;
            document.querySelector(".comic-2-3").innerHTML = data.comic23;
            document.querySelector(".cta-description").innerHTML = data.ctaDescription;
            document.querySelector(".cta-button").innerHTML = data.ctaButton;

            // Change button language
            document.querySelector(".language-button").innerHTML = lang === "en" ? "EN" : "RU";
        })
        .catch(error => console.error('Error loading language content:', error));
}

function switchLanguage() {
    currentLanguage = currentLanguage === "en" ? "ru" : "en";
    loadLanguageContent(currentLanguage);
}

document.addEventListener('DOMContentLoaded', function () {
    loadLanguageContent(currentLanguage);
});
