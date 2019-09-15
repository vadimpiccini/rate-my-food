

$(document).ready(function (){
 var originalwidth = $("#starcorner").width();
 $("#starfull").bind("mousemove",function(e){
  var offset = $("#starfull").offset();
  var clickX=e.clientX - offset.left;
  var clickY=e.clientY - offset.top;

    if((clickX>=0&&clickX<=55)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("20%");
     }
    if((clickX>=56&&clickX<=119)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("40%");
    }
    if((clickX>=120&&clickX<=177)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("60%");
    }
    if((clickX>=178&&clickX<=235)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("80%");
    }
    if((clickX>=236&&clickX<=290)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("100%");
    }


});


$("#starfull").mouseleave(function(){
 $("#starcorner").width(originalwidth);

});
});




$(document).ready(function(){

 var originalwidth = $("#starcorner").width();
 $("#starblank").bind("mousemove",function(e){
  var offset = $("#starblank").offset();
  var clickX=e.clientX - offset.left;
  var clickY=e.clientY - offset.top;

    if((clickX>=0&&clickX<=55)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("20%");
    }
    if((clickX>=56&&clickX<=119)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("40%");
    }
    if((clickX>=120&&clickX<=177)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("60%");
    }
    if((clickX>=178&&clickX<=235)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("80%");
    }
    if((clickX>=236&&clickX<=290)&&(clickY>=0&&clickY<=50))
    {
     $("#starcorner").width("100%");
    }

$("#starblank").mouseleave(function(){
 $("#starcorner").width(originalwidth);

});

});
});







$(document).ready(function (){
 var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
 $("#starfull").bind("click",function(e){
  var offset = $("#starfull").offset();
  var clickX=e.clientX - offset.left;
  var clickY=e.clientY - offset.top;

    if((clickX>=0&&clickX<=55)&&(clickY>=0&&clickY<=50))
    {
     $.post("/rate", { star: "1", recipe_id: getUrlParameter('id')}, $("#successrate").text(
      "You have rated this recipe 1/5!"));
    }

    if((clickX>=56&&clickX<=119)&&(clickY>=0&&clickY<=50))
    {
     $.post("/rate", { star: "2", recipe_id: getUrlParameter('id')}, $("#successrate").text(
      "You have rated this recipe 2/5!"));
    }
    if((clickX>=120&&clickX<=177)&&(clickY>=0&&clickY<=50))
    {
      $.post("/rate", { star: "3", recipe_id: getUrlParameter('id')}, $("#successrate").text(
      "You have rated this recipe 3/5!"));
      }
    if((clickX>=178&&clickX<=235)&&(clickY>=0&&clickY<=50))
    {
     $.post("/rate", { star: "4", recipe_id: getUrlParameter('id')}, $("#successrate").text(
      "You have rated this recipe 4/5!"));
    }
    if((clickX>=236&&clickX<=290)&&(clickY>=0&&clickY<=50))
    {
     $.post("/rate", { star: "5", recipe_id: getUrlParameter('id')}, $("#successrate").text(
      "You have rated this recipe 5/5!"));
    }

});
});