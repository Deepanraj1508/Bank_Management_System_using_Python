//jQuery time
var current_fs, next_fs, previous_fs; 	//fieldsets
var left, opacity, scale; 		//fieldset properties which we will animate
var animating; 				//flag to prevent quick multi-click glitches

$(".next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	next_fs = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
			'transform': 'scale('+scale+')',
			'position': 'absolute'
      		});
		     next_fs.css({'left': left, 'opacity': opacity});
		},
		
		duration: 500, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		}, 
		duration: 600, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
	
		easing: 'easeInOutBack'
	});
});

$(document).ready(function() {
    // Example of using the "easeOutCubic" easing function
    $("div").animate({
        left: '250px',
        // opacity: '0.5'
    }, {
        duration: 2000,
        easing: 'easeOutCubic',
        complete: function() {
            // Animation complete callback
            console.log("Animation complete");
        }
    });
});

$(".submit").click(function(){
    // Prevent the default form submission behavior
    event.preventDefault();

    // Submit the form using AJAX
    $.ajax({
        type: "POST",
        url: "/customer_registration",  // Specify the Flask route URL for form submission
        data: $("form").serialize(), // Serialize the form data
        success: function(response) {
            // Redirect to home.html page after successful form submission
            window.location.href = "/customerlogin";
        },
        error: function(xhr, status, error) {
            // Handle errors if any
            console.error(error);
        }
    });
});

