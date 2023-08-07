$(document).ready(() => {

    $("#slider").on("input change", (e) => {
        const sliderPos = e.target.value;
        // Update the width of the foreground image
        $('.foreground-img').css('width', `${sliderPos}%`)
        // Update the position of the slider button
        $('.slider-button').css('left', `calc(${sliderPos}% - 18px)`)
    });

    $("#file_antigo").on("change", () => {
        let path = $('#file_antigo').val()
        $('.background-img').css("background-image", `url(${path})`)
    });
    $("#file_novo").on("change", () => {
        let path = $('#file_novo').val()
        $('.foreground-img').css("background-image", `url(${path})`)
    });

});