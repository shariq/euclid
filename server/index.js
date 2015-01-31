$(document).ready(function() {

    var loaded = [4];
    var intervalVar;

    function hmmDotting() {
        if (loaded[0] > 0) {
            $('#course')[0].textContent = 'JAHA';
            $('#title')[0].textContent = 'o' + ['.', '..', '...', '....'][4 - loaded[0]] + 'O';
            $('#timing')[0].textContent = ['-', '--', '---', '---'][4 - loaded[0]];
            $('#about')[0].textContent = ['__', '___', '____', '_____'][4 - loaded[0]];
//            $('#description')[0].textContent = 'Hmm' + ['', '.', '..', '...'][4 - loaded[0]];
            loaded[0] = loaded[0] - 1;
        } else {
            clearInterval(intervalVar);
        }
    }

    intervalVar = window.setInterval(function() {
        hmmDotting();
    }, 300);

    last_course = ['HUMAN'];

    function changeClass() {
        $.get('/random', function(data) {
            loaded[0] = 0;
            json_data = JSON.parse(data);
            if (json_data['course'] == 'n/a') {
                $('#course')[0].textContent = 'XD';
                $('#title')[0].textContent = ':-(';
                $('#timing')[0].textContent = 'nothing';
                $('#about')[0].textContent = 'left';
//                $('#description')[0].textContent = '';
                last_course[0] = json_data['course'];
                return;
            }
            if (last_course[0] == json_data['course']) {
                changeClass();
                return;
            }
            last_course[0] = json_data['course'];
            course = json_data['course'];
            title = json_data['title'];
            timing = json_data['start_s'] + ' - ';
            timing += json_data['end_s'] + ' in ';
            timing += json_data['location'];
            about = json_data['type'] + ' with ';
            about += json_data['size'] + ' seat';
            if (json_data['size'] > 0) {
                about += 's';
            }
            $('#title')[0].textContent = title;
            $('#course')[0].textContent = course;
            $('#timing')[0].textContent = timing;
            $('#about')[0].textContent = about;
//            $('#description')[0].textContent = json_data['description'];
            clearInterval(intervalVar);
        });
    }

    function adjustFont() {
        windowWidth = parseInt($('html').css('width').replace('px',''));
        if (windowWidth > 850) windowWidth = 850;
        $('#course').css('font-size', windowWidth/7.5 + "px");
        $('#title').css('font-size', windowWidth/22.5 + "px");
        $('#timing').css('font-size', windowWidth/22.5 + "px");
        $('#about').css('font-size', windowWidth/22.5 + "px");
//        $('#description').css('font-size', windowWidth/30 + "px");
    }

    adjustFont();
    changeClass();

    $(window).resize(adjustFont);
    $(document).keypress(changeClass);
    $$('body').tap(changeClass);
});
