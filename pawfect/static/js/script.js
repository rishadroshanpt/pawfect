new Swiper('.card-wrapper', {
    loop: true,
    spaceBetween:30,
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints:{
        0:{
            slidesPerView:1
        },
        768:{
            slidesPerView:3
        },
        1024:{
            slidesPerView:4
        },
    }
  });
  