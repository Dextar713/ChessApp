$("document").ready(function() {
    var timer_white = new Date(), timer_black = new Date(), extra = 0;
    var interval_white, interval_black, interval;
    var game_over = false;
    var color = 'White';
    init_timer();
    display_time();
    start_timer();
    var board;
    var left, right;
    var top, bottom;
    var w, h;
    var w2, h2;
    var dim;
    $(window).on("resize", function() {
        var hf = 0.09 * ($(window).height() - 2 * $("#mynav > nav").height());
        //alert($("#mynav > nav").height());
        var wf = 0.05 * $(window).width();
        dim = Math.min(hf, wf);
        $("td.field").height(dim);
        $("td.field").width(dim);
        $(".figure > img").height(dim);
        $(".figure > img").width(dim);
        board = $(".board")[0].getBoundingClientRect();
        left = board.left; right = board.right;
        top = board.top; bottom = board.bottom;
        w = right - left; h = bottom - top;
        w2 = w / 8; h2 = h/8;
    }).trigger('resize');
    //$("td.field").height();
    // var board = $(".board")[0].getBoundingClientRect();
    // var left = board.left, right = board.right;
    // var top = board.top, bottom = board.bottom;
    // var w = right - left, h = bottom - top;
    // var w2 = w / 8, h2 = h/8;
    //var prevx = 0, prevy = 0;
    //alert(left+" "+right+"   "+top+" "+bottom+" ");
    function set_drag() {
        $(".figure").draggable({
            stop: function(event, ui) {
                var prevx = get_prevx(event), prevy = get_prevy(event);
                //alert(prevx+" "+prevy); 
                var curx = getx(event), cury = gety(event);
                //alert(event.pageX + " " +event.pageY + " " + curx + " " + cury);
                //alert(curx+"  "+cury);
                fetch(`${window.origin}/game`, {
                    method: 'post',
                    credentials: 'include',
                    body: JSON.stringify({
                        'prevx': prevx,
                        'prevy': prevy,
                        'curx': curx,
                        'cury': cury
                    }),
                    cache: 'no-cache',
                    headers: new Headers({
                        'content-type': "application/json"
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if(data.success) {
                        if(color==='White') {
                            timer_white.setSeconds(timer_white.getSeconds() + extra);
                            color = 'Black';
                        } else {
                            timer_black.setSeconds(timer_black.getSeconds() + extra);
                            color = 'White';
                        }
                        var prev_selector = "#f" + prevx + "" + prevy;
                        var cur_selector = "#f" + curx + "" + cury;
                        $(prev_selector).html("");
                        cur_html = '<div class="figure"><img src="' + data.img + '" height="100%" width="100%"></div>'
                        $(cur_selector).html(cur_html);
                    } else {
                        var prev_selector = "#f" + prevx + "" + prevy;
                        prev_html = '<div class="figure"><img src="' + data.img + '" height="100%" width="100%"></div>'
                        $(prev_selector).html(prev_html);
                        event.target.remove();
                        //alert("Impossible");
                    }
                    if(data.game_over) {
                        game_over = true;
                        //data.winner;
                    }
                    set_drag();
                })
                
            }
        })
    };

    set_drag();

    function get_prevx(event) {
        return parseInt(event.target.parentElement.id.charAt(1));
    };

    function get_prevy(event) {
        return parseInt(event.target.parentElement.id.charAt(2));
    };

    function getx(event) {
        return parseInt((event.pageX - left) / w2);
    };

    function gety(event) {
        return parseInt((bottom - event.pageY) / h2);
    };

    function init_timer() {
        var mode = $("div.timer h2").text();
        var [mins, secs] = mode.split(':');
        //alert(mins);
        extra = parseInt(secs);
        timer_white.setMinutes(mins);
        timer_black.setMinutes(mins);
        timer_white.setSeconds(0);
        timer_black.setSeconds(0);
    };

    function time_to_text() {
        var text_white = '0';
        if(timer_white.getMinutes()<10) {
            text_white += timer_white.getMinutes();
        } else {
            text_white = timer_white.getMinutes();
        }
        text_white += ':';
        if(timer_white.getSeconds()<10) {
            text_white += '0' + timer_white.getSeconds();
        } else {
            text_white += timer_white.getSeconds();
        }

        var text_black = '0';
        if(timer_black.getMinutes()<10) {
            text_black += timer_black.getMinutes();
        } else {
            text_black = timer_black.getMinutes();
        }
        text_black += ':';
        if(timer_black.getSeconds()<10) {
            text_black += '0' + timer_black.getSeconds();
        } else {
            text_black += timer_black.getSeconds();
        }
        return [text_white, text_black];
    }

    function display_time() {
        var time_text = time_to_text();
        $(".timer_up h2").text(time_text[1]);
        $(".timer_down h2").text(time_text[0]);
    };

    function count_down() {
        if(color==='White') {
            timer_white.setSeconds(timer_white.getSeconds() - 1);
        } else {
            timer_black.setSeconds(timer_black.getSeconds() - 1);
        }
        display_time();
        var time_expired = false;
        if(timer_white.getMinutes()==0&&timer_white.getSeconds()==0) {
            time_expired = true;
            clearInterval(interval);
        } else if(timer_black.getMinutes()==0&&timer_black.getSeconds()==0) {
            time_expired = true;
            clearInterval(interval);
        }
        if(time_expired) {
            fetch(`${window.origin}/game`, {
                method: 'post',
                credentials: 'include',
                body: JSON.stringify({
                    'time_expired': color
                }),
                cache: 'no-cache',
                headers: new Headers({
                    'content-type': "application/json"
                })
            })
            .then(respnse => response.json())
            .then(data => {
                alert(data.winner);
            })
        }
    };

    function start_timer() {
        interval = setInterval(count_down, 1000);
    };

});