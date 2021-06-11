
function changeSlide()
{
  var slide = document.querySelector('#id_slot');
$("#value_slot").html(slide.value);
$("#money").html((slide.value*30000).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
}
$("#value_slot").html(slide.value);
$("#money").html((slide.value*30000).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));