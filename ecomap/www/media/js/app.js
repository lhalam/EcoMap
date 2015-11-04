  var toogle=document.getElementById("toggle");
  var filter=document.getElementById("filter");
  console.log(toogle);
  toogle.addEventListener("click" , function () {
   filter.classList.toggle("toggle_hide");
  });

  var inform_probl_block=document.getElementsByClassName("inform_probl_block")[0];
  var inform_probl_btn=document.getElementById("inform_probl_btn");
  inform_probl_btn.addEventListener("click",function (ev){
    inform_probl_block.classList.toggle("hide_probl_block")
  })

  var registr_block=document.getElementsByClassName("registr_block")[0]

  var registration_btn=document.getElementById("registration")
  registration.addEventListener("click",function (){
    
    registr_block.classList.toggle("visibible")
  })



  $(document).add(".okay").click(function() {
    $(".message").removeClass("active");
  });

