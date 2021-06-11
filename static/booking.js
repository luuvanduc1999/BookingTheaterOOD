function price()
{
  if ($('input[name="type"]:checked').val()=="3D") {return(30000);}
  else if ($('input[name="type"]:checked').val()=="2D") {return(20000);}
  else return(0);
  
}

function changeSlide()
{
  var slide = document.querySelector('#id_slot');
  $("#value_slot").html(slide.value);
  $("#money").html((slide.value*price()).toFixed(0).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
}
$("#value_slot").html(slide.value);
$("#money").html((slide.value*price()).toFixed(0).replace(/\d(?=(\d{3})+\.)/g, '$&,'));