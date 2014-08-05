$(function () {

    function blink_background($el){

        /* adaptado de: http://stackoverflow.com/a/15681223/1503 */
        var x = 300;
        var originalColor = $el.css("background-color");
        var new_color = '#B3D4FC';
        var i = 3; //counter

        (function loop() { //recurisve IIFE
            $el.css("background-color", new_color);
            setTimeout(function () {
                $el.css("background-color", originalColor);
                if (--i) setTimeout(loop, x); //restart loop
            }, x);
        }());

    }

    $("a.error_message").click(function(event){
        event.preventDefault();
        var code_block = $('#code-block');
        $('html, body').animate(
            { scrollTop: code_block.offset().top },
            200
        );
        var search_term = $(this).data('search-term');
        var exact_search_term = "<!--SPS-ERROR: " + search_term + "-->";
        /* token is a span contains the SPS-ERROR message */
        var token = $('span.token.comment').filter("*:contains('" + exact_search_term + "')");
        /* scroll to token */
        code_block.scrollTo(
            token,
            300,
            {
                axis: 'y',
                offset: function() { return {top:-45, left:0}; },
                onAfter: function(){
                    blink_background(token);
                }
            }
        )
    });

    $("#back-to-errors").click(function(event){
        event.preventDefault();
        var table = $('#validation_errors_table')
        $('html, body').animate(
            { scrollTop: table.offset().top - 100 },
            200
        );
    });

});
