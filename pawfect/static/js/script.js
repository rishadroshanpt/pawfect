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
            slidesPerView:3,
            spaceBetween: 40,

        },
        768:{
            slidesPerView:4,
            spaceBetween: 40,

        },
        1024:{
            slidesPerView:5,
            spaceBetween: 40,

        },
    }
  });

