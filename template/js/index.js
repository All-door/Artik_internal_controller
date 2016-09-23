$('#save').on('click', function (e) {

  var ssid = $("#ssid").val();
  var password = $("#password").val();
  var all_door_id = $("#all_door_id").val();
  var artik_cloud_id = $("#artik_cloud_id").val();
  var master_pw = $("#master_pw").val();

  url = "save/"+ssid+"/"+password+"/"+all_door_id+"/"+artik_cloud_id+"/"+master_pw;

  $.get(url);
  alert("설정이 완료되었습니다.");
});


$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});
