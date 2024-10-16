document.addEventListener("DOMContentLoaded", function () {
    // Анимация прокрутки для появления элементов
    const scrollElements = document.querySelectorAll(".appear-on-scroll");

    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;

        return (
            elementTop <=
            (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };

    const displayScrollElement = (element) => {
        element.classList.add("appear");
    };

    const hideScrollElement = (element) => {
        element.classList.remove("appear");
    };

    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.25)) {
                displayScrollElement(el);
            }
        });
    };

    // Плавное появление элементов после полной загрузки страницы
    window.addEventListener("scroll", handleScrollAnimation);
    handleScrollAnimation(); // Запуск сразу при загрузке страницы для появления элементов, которые уже видны

    // Плавное появление контента hero-section после загрузки страницы
    const heroContent = document.querySelector(".hero-content");
    if (heroContent) {
        heroContent.classList.add("appear");
    }

    const loadLanguage = (lang) => {
        fetch(`locales/${lang}.json`)
            .then(response => response.json())
            .then(data => {
                document.querySelector('.hero-content h1').textContent = data.heroTitle;
                document.querySelector('.hero-content p').textContent = data.heroDescription;
                document.querySelector('.cta-button').textContent = data.ctaButton;
                document.querySelector('.tokenomics-section h2').textContent = data.tokenomicsTitle;
                document.querySelector('.token-box:nth-child(1) h3').textContent = data.totalSupplyTitle;
                document.querySelector('.token-box:nth-child(1) p').textContent = data.totalSupplyText;
                document.querySelector('.token-box:nth-child(2) h3').textContent = data.distributionTitle;
                document.querySelector('.token-box:nth-child(2) p').textContent = data.distributionText;
                document.querySelector('.token-box:nth-child(3) h3').textContent = data.initialPriceTitle;
                document.querySelector('.token-box:nth-child(3) p').textContent = data.initialPriceText;
                document.querySelector('.whitepaper-content h2').textContent = data.whitepaperTitle;
                document.querySelector('.whitepaper-excerpt p').textContent = data.whitepaperContent;
                document.querySelector('.whitepaper-link').textContent = data.whitepaperLink;
                document.querySelector('.whitepaper-excerpt h3').textContent = data.whitepaperContentsTitle;
                const contentsList = document.querySelector('.whitepaper-excerpt ul');
                contentsList.innerHTML = ''; // Очистка текущего списка
                data.whitepaperContents.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.textContent = item;
                    contentsList.appendChild(listItem);
                });
            })
            .catch(error => console.error('Error loading language file:', error));
    };

    // Функция для переключения языка
    window.switchLanguage = () => {
        const currentLanguage = document.documentElement.lang;
        const newLanguage = currentLanguage === 'en' ? 'ru' : 'en';
        document.documentElement.lang = newLanguage;

        // Меняем надпись на кнопке смены языка
        const languageButton = document.querySelector('.language-button');
        languageButton.textContent = newLanguage.toUpperCase();

        // Загружаем тексты на выбранном языке
        loadLanguage(newLanguage);
    };

    // Изначальная загрузка языка
    const initialLanguage = document.documentElement.lang || 'en';
    loadLanguage(initialLanguage);

    // Устанавливаем текст кнопки языка при загрузке
    const languageButton = document.querySelector('.language-button');
    languageButton.textContent = initialLanguage.toUpperCase();
});
