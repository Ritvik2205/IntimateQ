window.addEventListener('scroll', function() {
    const image = document.querySelector('img');
    const scrollPosition = window.scrollY;
    const scale = Math.max(1 - scrollPosition / 1000, 0.5);

    image.style.transform = `translateX(-50%) scale(${scale})`;
    
    const initialTop = (window.innerHeight - image.clientHeight) / 2;
    const finalTop = 0;
    const top = Math.max(finalTop, initialTop - scrollPosition);

    image.style.top = `${Math.max(top, 0)}px`;
    image.classList.toggle('sticky', window.scrollY > 0);
});